import requests
import json

# url = 'https://www.zyxware.com/articles/4344/list-of-fortune-500-companies-and-their-websites'
# r = requests.get(url)
# txt = r.text
# lst = txt.split('td')
# data = []
# for i in range(5, 318, 3):
# 	if 'href' in lst[i]:
# 		data.append(lst[i].split('href="')[1].split('">')[0])

# with open('urls.txt','w') as f:
# 	[f.write(i+'\n') for i in data]

url = 'https://hackerone.com/graphql'
# json = {
#   "operationName": "DiscoveryQuery",
#   "variables": {
#     "where": {
#       "_and": [
#         {
#           "type": {
#             "_neq": "Assessment"
#           }
#         },
#         {
#           "_or": [
#             {
#               "submission_state": {
#                 "_eq": "open"
#               }
#             },
#             {
#               "submission_state": {
#                 "_eq": "api_only"
#               }
#             },
#             {
#               "external_program": {}
#             }
#           ]
#         },
#         {
#           "team_industry": {
#             "industry": {
#               "_eq": "Internet & Online Services"
#             }
#           }
#         }
#       ]
#     },
#     "secureOrderBy": {
#       "launched_at": {
#         "_direction": "DESC"
#       }
#     }
#   },
#   "query": "query DiscoveryQuery($cursor: String, $where: FiltersTeamFilterInput, $secureOrderBy: FiltersTeamFilterOrder) {\n  me {\n    id\n    ...OpportunityListMe\n    __typename\n  }\n  teams(first: 100, where: $where, after: $cursor, secure_order_by: $secureOrderBy) {\n    pageInfo {\n      endCursor\n      hasNextPage\n      __typename\n    }\n    ...SearchSummaryTeamConnection\n    ...OpportunityListTeamConnection\n    __typename\n  }\n}\n\nfragment OpportunityListTeamConnection on TeamConnection {\n  edges {\n    node {\n      id\n      ...OpportunityCardTeam\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment OpportunityCardTeam on Team {\n  id\n  name\n  handle\n  profile_picture(size: small)\n  triage_active\n  publicly_visible_retesting\n  allows_private_disclosure\n  allows_bounty_splitting\n  launched_at\n  state\n  offers_bounties\n  external_program {\n    id\n    __typename\n  }\n  last_updated_at\n  currency\n  type\n  minimum_bounty_table_value\n  maximum_bounty_table_value\n  response_efficiency_percentage\n  first_response_time\n  ...ResponseEfficiencyIndicator\n  ...BookmarkTeam\n  ...ScopeTeam\n  team_display_options {\n    id\n    show_response_efficiency_indicator\n    __typename\n  }\n  __typename\n}\n\nfragment ResponseEfficiencyIndicator on Team {\n  id\n  response_efficiency_percentage\n  __typename\n}\n\nfragment BookmarkTeam on Team {\n  id\n  bookmarked\n  __typename\n}\n\nfragment ScopeTeam on Team {\n  id\n  structured_scope_stats\n  __typename\n}\n\nfragment OpportunityListMe on User {\n  id\n  ...OpportunityCardMe\n  __typename\n}\n\nfragment OpportunityCardMe on User {\n  id\n  ...BookmarkMe\n  __typename\n}\n\nfragment BookmarkMe on User {\n  id\n  __typename\n}\n\nfragment SearchSummaryTeamConnection on TeamConnection {\n  total_count\n  __typename\n}\n"
# }

json = {
  "operationName": "DiscoveryQuery",
  "variables": {
    "where": {
      "_and": [
        {
          "type": {
            "_neq": "Assessment"
          }
        },
        {
          "_or": [
            {
              "submission_state": {
                "_eq": "open"
              }
            },
            {
              "submission_state": {
                "_eq": "api_only"
              }
            },
            {
              "external_program": {}
            }
          ]
        }
      ]
    },
    "secureOrderBy": {
      "launched_at": {
        "_direction": "DESC"
      }
    }
  },
  "query": "query DiscoveryQuery($cursor: String, $where: FiltersTeamFilterInput, $secureOrderBy: FiltersTeamFilterOrder) {\n  me {\n    id\n    ...OpportunityListMe\n    __typename\n  }\n  teams(first: 100, where: $where, after: $cursor, secure_order_by: $secureOrderBy) {\n    pageInfo {\n      endCursor\n      hasNextPage\n      __typename\n    }\n    ...SearchSummaryTeamConnection\n    ...OpportunityListTeamConnection\n    __typename\n  }\n}\n\nfragment OpportunityListTeamConnection on TeamConnection {\n  edges {\n    node {\n      id\n      ...OpportunityCardTeam\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment OpportunityCardTeam on Team {\n  id\n  name\n  handle\n  profile_picture(size: small)\n  triage_active\n  publicly_visible_retesting\n  allows_private_disclosure\n  allows_bounty_splitting\n  launched_at\n  state\n  offers_bounties\n  external_program {\n    id\n    __typename\n  }\n  last_updated_at\n  currency\n  type\n  minimum_bounty_table_value\n  maximum_bounty_table_value\n  response_efficiency_percentage\n  first_response_time\n  ...ResponseEfficiencyIndicator\n  ...BookmarkTeam\n  ...ScopeTeam\n  team_display_options {\n    id\n    show_response_efficiency_indicator\n    __typename\n  }\n  __typename\n}\n\nfragment ResponseEfficiencyIndicator on Team {\n  id\n  response_efficiency_percentage\n  __typename\n}\n\nfragment BookmarkTeam on Team {\n  id\n  bookmarked\n  __typename\n}\n\nfragment ScopeTeam on Team {\n  id\n  structured_scope_stats\n  __typename\n}\n\nfragment OpportunityListMe on User {\n  id\n  ...OpportunityCardMe\n  __typename\n}\n\nfragment OpportunityCardMe on User {\n  id\n  ...BookmarkMe\n  __typename\n}\n\nfragment BookmarkMe on User {\n  id\n  __typename\n}\n\nfragment SearchSummaryTeamConnection on TeamConnection {\n  total_count\n  __typename\n}\n"
}

def fetch_companies(companies, cursor):
	if (cursor != None):
		json['variables']['cursor'] = cursor

	# headers = {'Authorization': 'token %s' % api_token}
	res = requests.post(url, json = json).json()
	for entry in res['data']['teams']['edges']:
		companies.append([entry['node']['name'], entry['node']['handle']])
	return res['data']['teams']['pageInfo']['endCursor']

def fetch_urls():
	companies = []
	cursor = None
	headers = {'Accept': 'application/json'}

	for i in range(61):
		cursor = fetch_companies(companies, cursor)

	print(len(companies))
	urls = []
	for lst in companies:
		# print(lst)
		res = requests.get('https://hackerone.com/' + lst[1], headers = headers).json()
		urls.append(res['profile']['website'])
	return urls


urls = fetch_urls()
print(len(urls))
with open('urls.txt','w') as f:
	[f.write(url+'\n') for url in urls]

