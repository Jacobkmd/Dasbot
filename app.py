import dasbot
import yaml
import os

if __name__ == '__main__':
    
    dispatchers = []
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
    
    with open(os.path.join(__location__, 'jobs.yaml'), 'r') as stream:
        jobs = yaml.safe_load(stream)
                
        for job in jobs['UpdateConfluenceCalender']['ConfluencePages']:
            confluence_id = jobs['UpdateConfluenceCalender']['ConfluencePages'][job]['Confluence_id']
            unit = jobs['UpdateConfluenceCalender']['ConfluencePages'][job]['Unit']

            dispatcher = dasbot.update_confluence_calender_page(confluence_id, unit)

            if jobs['UpdateConfluenceCalender']['ConfluencePages'][job]['Include_in_summary_page'] is True:
                dispatchers.append(dasbot.Dispatcher(job, dispatcher))

        if jobs['UpdateConfluenceCalender']['Summary_page_id'] is not None:
            #todo; add dispatchers > 0 
            confluence_id = jobs['UpdateConfluenceCalender']['Summary_page_id']
            dasbot.update_confluence_summary_page(confluence_id, dispatchers)


        for job in jobs['SearchDomain']:
            domain = jobs['SearchDomain'][job]['Domain']
            
            html = dasbot.htmlparser.get_html_from_browser('https://www.webhuset.no/bestillingsskjema/domenesok?coupon-2=&fqdn='+ domain, 3)
            status = dasbot.htmlparser.get_text_from_tagname(html, 'div', 'col-xs-12 result-text').strip()
            print(domain + ": " + status)

            if status.find("ledig") != -1:
                email = jobs['SearchDomain'][job]['Email']
                dasbot.send_email(email, domain + " er ledig!", "")


        for job in jobs['ChangeJiraIssueTransition']:
            jql = jobs['ChangeJiraIssueTransition'][job]['Jql']
            to_status = jobs['ChangeJiraIssueTransition'][job]['ToStatus']
            
            jira_issues = dasbot.jira.jql(jql)
                        
            for jira_issue in jira_issues["issues"]:
                dasbot.jira.set_issue_status_by_transition_id(jira_issue["key"], to_status)
                print(jira_issue["key"] + " er flyttet..")
                