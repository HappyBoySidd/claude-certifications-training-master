#!/usr/bin/env python3
"""Fixed-fixture calculations and authored reference decisions. Not a policy executor or general-purpose validator; no Claude/API/MCP runtime is invoked."""
import argparse,json
from pathlib import Path
FIXTURES=json.loads(Path(__file__).with_name('benchmark-fixtures.json').read_text())['records']
def inspect(k,x):
 if k=='1.1':return {'tool_request_ids':[r['id'] for r in x['responses'] if r.get('stop_reason')=='tool_use'],'failed_result_ids':[r['tool_result_for'] for r in x['responses'] if r.get('status')=='timeout'],'last_stop':x['responses'][-1]['stop_reason'],'business_complete':x['task_complete'],'next_policy':'bounded continuation or documented partial stop; not success'}
 if k=='1.2':return {'missing':sorted(set(x['required'])-set(x['returned'])),'complete':set(x['required'])<=set(x['returned'])}
 if k=='1.3':return {'source_attributable':bool(x['finding']['locator']),'parent_context_available':x['prior_context'] is not None,'allowed_tools':x['allowed_tools'],'repair_required':['task','source locator','tool boundary']}
 if k=='1.4':return {'account_matches':x['approval']['account']==x['proposed']['account'],'amount_matches':x['approval']['amount_minor']==x['proposed']['amount_minor'],'not_expired':x['proposed']['time']<x['approval']['expires'],'submit':False}
 if k=='1.5':return {'pre_denial_service_calls':x['service_call_count_before'],'post_detection_service_calls':1,'post_detection_undo_proven':False}
 if k=='1.6':return {'jobA':'fixed dependency workflow','jobB':'adaptive investigation','integration_review_required':True}
 if k=='1.7':return {'file_changed':x['checkpoint']['file_digest']!=x['current']['file_digest'],'approval_current':x['current']['approval']!='expired','revalidate':['changed file','action authority'],'candidate_reuse':x['unchanged_tasks']}
 if k=='2.1':return {'request_count':len(x['requests']),'oracle_read_count':x['oracle'].count('read_status'),'oracle_write_count':x['oracle'].count('issue_credit'),'observed_choices':None,'observed_accuracy':None,'reason':'No model routing run performed; compare actual choices with this oracle later'}
 if k=='2.2':return {'classification':['protocol error: unknown tool','execution error: denied','execution error: timeout','success: empty matches'],'retry_candidate_indexes':[2],'empty_is_failure':False}
 if k=='2.3':return {'retain':x['needs'],'remove':x['unneeded'],'role':x['role']}
 if k=='2.4':return {'configuration_scope':x['scope'],'secret_value_in_fixture':False,'provisioned':x['token_provisioned'],'connected':x['server_connected'],'resource_included':x['resource_read'],'integration_proven':False}
 if k=='2.5':return {'inspect_order':[x['entry']]+x['export_chain']+[x['test_path']],'target':x['target'],'unscoped_replace_safe':False,'call_sites_observed':False}
 if k=='3.1':return {'home_rule_distributed':x['new_teammate_has_home_rules'],'project_conflict':len(x['repo_rules'])>1,'repair':'repository-shared reconciled guidance','settings_precedence_tested':False}
 if k=='3.2':return {'procedure':x['workflow'],'argument':x['argument'],'universal_rule':x['universal_rule'],'requested_capability':x['required_capability'],'runtime_isolation_verified':False,'runtime_permissions_verified':False}
 if k=='3.3':
  from pathlib import PurePosixPath
  return {'match_path':PurePosixPath(x['match']).match(x['rule_path']),'nonmatch_path':PurePosixPath(x['nonmatch']).match(x['rule_path']),'isolated_sessions':len(set(x['sessions']))==2,'actual_guidance_loading_observed':False}
 if k=='3.4':return {'taskA':'bounded edit plus check','taskB':'resolve design and rollback first','line_count_is_sole_rule':False}
 if k=='3.5':return {'known_numeric_zero':x['examples'][0]['output'],'known_empty_string':x['examples'][1]['output'],'string_zero_result':None,'requires_clarification':True}
 if k=='3.6':return {'digest_matches':x['review_digest']==x['candidate_digest'],'accept':x['review_digest']==x['candidate_digest'],'policy':x['policy'],'process_success_implies_review_pass':False}
 if k=='4.1':return {'report':['reachable null dereference'],'suppress':['style difference'],'needs_evidence':['comment mismatch'],'review_detection_run':False}
 if k=='4.2':return {'source_layouts':len(x['source_examples']),'unseen_layout':x['unseen'],'record_rule':x['format'],'unseen_accuracy_observed':False}
 if k=='4.3':return {'shape_pass':x['schema_valid'],'amount_supported':x['output']['amount_minor']==x['source_supported_amount_minor'],'reference_unknown_preserved':x['output']['reference'] is None,'accept':False}
 if k=='4.4':return {'computed_sum':sum(x['line_items']),'stated_total':x['stated_total'],'mismatch':sum(x['line_items'])!=x['stated_total'],'retry_budget':x['retry_budget'],'invent_missing_item':False,'preserve_failed_output':True}
 if k=='4.5':return {'joined':{k:x['outcomes'][k] for k in x['input_ids']},'preserve':['D1'],'authorization_queue':['D2'],'retry':['D3'],'rerun_successes':False,'completion':'partial'}
 if k=='4.6':
  import re
  minor=int(re.search(r'amount_minor=(\d+)',x['fixture_A']).group(1));expected=minor/100;actual=minor
  return {'expected_usd':expected,'actual_usd':actual,'factor_error':actual/expected,'local_integer_checks_sufficient':False,'independent_reviewer_detection_observed':False}
 if k=='5.1':return {'retained':x['facts'],'summary_sufficient':False,'required_fact_keys':sorted(x['facts'])}
 if k=='5.2':return {'actions':['normal lookup with empathy','human handoff','identity clarification before account action','authorized policy escalation'],'guess_account':False,'invent_policy':False}
 if k=='5.3':return {'preserve':[k for k,v in x['specialists'].items() if 'success' in v],'access_queue':[k for k,v in x['specialists'].items() if v.get('error')=='access_denied'],'retry':[k for k,v in x['specialists'].items() if v.get('error')=='timeout'][:x['remaining_retry_budget']],'complete':False}
 if k=='5.4':return {'source_changed':x['manifest']['source_digest']!=x['current_digest'],'history_finished':x['manifest']['finished'],'pending':x['manifest']['pending'],'fresh_acceptance_needed':True}
 if k=='5.5':return {'training':{r['segment']:r['correct']/r['n'] for r in x['training_bins']},'holdout':{r['segment']:r['correct']/r['n'] for r in x['separate_holdout']},'review_capacity':x['review_capacity'],'threshold_proven':False,'review_policy':'validate per segment on separate holdout; retain sampling'}
 if k=='5.6':return {'comparable_population':len({s['population'] for s in x['sources']})==1,'sources':x['sources'],'all_account_trend_supported':False,'average_incompatible_values':False}
 raise ValueError(k)
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--objective',choices=list(FIXTURES));p.add_argument('--input-only',action='store_true');p.add_argument('--self-test',action='store_true');a=p.parse_args()
 if a.self_test:
  for k,x in FIXTURES.items():
   z=inspect(k,x);assert isinstance(z,dict) and z
  assert inspect('1.2',FIXTURES['1.2'])['missing']==['migration']
  assert inspect('4.3',FIXTURES['4.3'])['amount_supported'] is False
  assert inspect('4.5',FIXTURES['4.5'])['retry']==['D3']
  assert inspect('5.5',FIXTURES['5.5'])['holdout']['handwritten_amount']==0.4
  print('30 offline fixture inspectors executed; four known-fixture assertions passed. No SDK, MCP, model-routing or learner mastery claim.');return
 if not a.objective:p.error('choose --objective or --self-test')
 x=FIXTURES[a.objective];out={'objective':a.objective,'input':x}
 if not a.input_only:out['fixed_fixture_calculations_and_reference_decisions']=inspect(a.objective,x);out['scope']='Mixture of controlled-fixture calculations and authored worked reference choices. No policy execution, generalized validation or live service/model evidence.'
 print(json.dumps(out,indent=2))
if __name__=='__main__':main()
