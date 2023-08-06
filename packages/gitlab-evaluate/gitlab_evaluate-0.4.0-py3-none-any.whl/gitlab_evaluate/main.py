#!/usr/bin/python3
import argparse
from gitlab_ps_utils.api import GitLabApi
from gitlab_ps_utils.json_utils import json_pretty
from gitlab_ps_utils.processes import MultiProcessing
from gitlab_evaluate.lib import api as api_helpers
from gitlab_evaluate.lib import utils
import logging

def get_all_project_data(my_dict, source, args, payload, headers, gitlabApi, csv_columns, csv_file, rollup_file, p):
  pid = p.get('id')
  statistics = p.get('statistics')
  if args.output:
    print('+' * 40)
    print(f"Name: {p.get('name')} ID: {pid}")
    print(f"Desc: {p.get('description')}")
  my_dict["Project"] = p.get('name')
  my_dict["ID"] = pid

  ## Get the full project info with stats
  
  full_stats_url = api_helpers.proj_info_get(pid, source)
  api_helpers.check_full_stats(full_stats_url, p, my_dict, headers={'private-token': args.token})

  #  TODO: This could be a dictionary of headers and functions eg:
  # boundaries = { 
  #   "Pipelines": {"threshold": 2500, "url": "/api/v4/projects/:id/pipelines"},
  #   "Issues":  {"threshold": 2500, "url": "/api/v4/projects/:id/issues"}
  # }

  # for k, v in boundaries.items():
  #   check_x_total_value_update_dict(p, k, v, my_dict, payload, headers)

  ## Get the `kind` of project - skip any that are of type `user`.

  # kind_url = api_helpers.proj_info_get(pid, source)
  # api_helpers.check_x_total_value_update_dict(utils.check_proj_type, p, kind_url, payload, headers, "Kind", my_dict)

  ## Get the number of pipelines per project
  flags = []
  pipelines_url = api_helpers.proj_pl_get(pid, source)
  flags.append(api_helpers.check_x_total_value_update_dict(utils.check_num_pl, p, pipelines_url, payload, headers, "Pipelines", "Pipelines_over", my_dict))

  ## Get number of issues per project
  issues_url = api_helpers.proj_issue_get(pid, source)
  flags.append(api_helpers.check_x_total_value_update_dict(utils.check_num_issues, p, issues_url, payload, headers, "Issues", "Issues_over", my_dict))
  
  ## Get number of branches per project
  branches_url = api_helpers.proj_branch_get(pid, source)
  flags.append(api_helpers.check_x_total_value_update_dict(utils.check_num_br, p, branches_url, payload, headers, "Branches", "Branches_over", my_dict))

  ## Get number of merge requests per project
  mrequests_url = api_helpers.proj_mr_get(pid, source)
  flags.append(api_helpers.check_x_total_value_update_dict(utils.check_num_mr, p, mrequests_url, payload, headers, "Merge Requests", "Merge Requests_over", my_dict))

  ## Get number of tags per project
  tags_url = api_helpers.proj_tag_get(pid, source)
  flags.append(api_helpers.check_x_total_value_update_dict(utils.check_num_tags, p, tags_url, payload, headers, "Tags", "Tags_over", my_dict))

  ## Get list of package types
  packages_in_use = set([x.get('package_type', '') 
    for x in gitlabApi.list_all(args.source, args.token, api_helpers.proj_packages_url(pid))])
  my_dict['Package Types In Use'] = ", ".join(packages_in_use) if packages_in_use else "N/A"

  if packages_in_use:
    flags.append(True)

  ## Get total packages size
  my_dict['Total Packages Size'] = utils.sizeof_fmt(statistics.get('packages_size'))
  
  ## Get container registry size
  my_dict['Container Registry Size'], flag_registries = api_helpers.get_registry_size(pid, args.source, args.token)
  if flag_registries:
    flags.append(True)

  dict_data = []
  dict_data.append({x: my_dict.get(x) for x in csv_columns})
  utils.write_to_csv(csv_file, csv_columns, dict_data, append=True)

  if True in flags:
    utils.write_to_csv(rollup_file, csv_columns, dict_data, append=True)

  if args.output:
    print(f"""
      {'+' * 40}
      {json_pretty(my_dict)}
    """)

  if args.output:
    print(json_pretty(my_dict))

def main():
  logging.basicConfig(filename='evaluate.log', level=logging.DEBUG)
  my_dict = {}
  csv_file = 'evaluate_output.csv'
  rollup_file = 'flags_evaluate_output.csv'
  csv_columns = [
    'Project',
    'ID',
    'kind',
    'Pipelines',
    'Pipelines_over',
    'Issues',
    'Issues_over',
    'Branches',
    'Branches_over',
    'commit_count',
    'commit_count_over',
    'Merge Requests',
    'Merge Requests_over',
    'storage_size',
    'storage_size_over',
    'repository_size',
    'repository_size_over',
    'Tags',
    'Tags_over',
    'Package Types In Use',
    'Total Packages Size',
    'Container Registry Size']
  parser = argparse.ArgumentParser()
  parser.add_argument("-t", "--token", help="Personal Access Token: REQ'd")
  parser.add_argument("-s", "--source", help="Source URL: REQ'd")
  parser.add_argument("-f", "--filename", help="CSV Output File Name. If not set, will default to 'evaluate_output.csv'")
  parser.add_argument("-o", "--output", action='store_true', help="Output Per Project Stats to screen")
  parser.add_argument("-i", "--insecure", action='store_true', help="Set to ignore SSL warnings.")
  parser.add_argument("-p", "--processes", help="Number of processes. Defaults to number of CPU cores")

  args = parser.parse_args()

  if None not in (args.token, args.source):
    processes = args.processes if args.processes else None
    ### Setup the csv file and write the headers.
    if args.filename:
      csv_file = args.filename
      rollup_file = f"flags_{args.filename}"
    utils.write_to_csv(csv_file, csv_columns, [])
    utils.write_to_csv(rollup_file, csv_columns, [])

    ### API and Headers - Setup URLs
    headers = {
        'private-token': args.token
    }

    payload = {
        'format': 'json'
    }

    app_api_url = "/application/statistics"
    project_api_url = "/projects?statistics=true"
    app_ver_url = "/version"
    source = args.source
    
    if args.insecure:
      gitlabApi = GitLabApi(ssl_verify=False)
      api_helpers.gl_api.ssl_verify=False
    else:
      gitlabApi = GitLabApi()

    if resp := api_helpers.getApplicationInfo(args.source,args.token,app_api_url):
      print('-' * 50)
      print(f'Basic information from source: {args.source}')
      # print("Status code:", 
      print("Total Merge Requests", resp.get('merge_requests'))
      print("Total Projects:", resp.get('projects'))
      print("total Forks:", resp.get('forks'))
      print('-' * 50)
    else:
      print(f"Unable to pull application info from URL: {args.source}")

    if resp := api_helpers.getVersion(args.source, args.token , app_ver_url):
      print('-' * 50)
      print("GitLab Source Ver:", resp.get('version'))
      print('-' * 50)
    else:
      print(f"Unable to pull application info from URL: {args.source}")
    
    mp = MultiProcessing()

    try:
      mp.start_multi_process_stream_with_args(get_all_project_data, 
        gitlabApi.list_all(args.source, args.token, project_api_url), 
        my_dict, 
        source, 
        args, 
        payload, 
        headers, 
        gitlabApi, 
        csv_columns, 
        csv_file, 
        rollup_file,
        processes=processes)
    except Exception as e:
      print(e)
      
  else:
    parser.print_help()

