import csv          # Used to read a .csv file.
import statistics

def createIssueIDMapping(og_issue_file, git_issue_file) -> dict[int,int]:
    """ Creates a mapping of Issue IDs
    :param og_issue_file: Original csv of issues
    :param git_issue_file: GitRE-generated csv of issues
    :return: A dictionary mapping issue IDs between original and generated issue CSVs
    """
    # Get Original Issue IDs
    titleToOrgID:dict[str,int] = {}
    line_count = 0
    with open(og_issue_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count == 0:
                if row != ['id', 'title', 'description']:
                    print("Row header incorrect for", filename)
                    quit()
                line_count += 1
            else:
                if row[1] in titleToOrgID:
                    print("Key error for", filename, "specifcally: ", row)
                    quit()
                titleToOrgID[row[1]] = int(row[0])
                line_count += 1

    issues_dict:dict[int,int] = {}  #git->org
    line_count = 0
    with open(git_issue_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count == 0:
                if row != ['id', 'title', 'description']:
                    print("Row header incorrect for", filename)
                    quit()
                line_count += 1
            else:
                try:
                    org_id:int = titleToOrgID[row[1]]
                    issues_dict[int(row[0])] = org_id
                except KeyError:
                    print("Error: Issue Key is missing: ", row[1])
                    quit()
                line_count += 1
    return issues_dict

def createSpecificationIDMapping(og_req_file,git_spec_file) -> dict[int,int]:
    """ Creates a mapping of specification IDs
    :param og_req_file: Original csv of requirements
    :param git_spec_file: GitRE-generated csv of requirements
    :return: A dictionary mapping specification IDs between original and generated requirement csvs
    """
    # Get Original Requirements IDs
    titleToOrgID:dict[str,int] = {}
    line_count = 0
    with open(og_req_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count == 0:
                if row != ['id', 'title', 'description']:
                    print("Row header incorrect for", filename)
                    quit()
                line_count += 1
            else:
                if row[1] in titleToOrgID:
                    print("Key error for", filename, "specifcally: ", row)
                    quit()
                titleToOrgID[row[1].strip()] = int(row[0])
                line_count += 1
    # for k,v in titleToOrgID.items():
    #     print(k,v)
    specs_dict:dict[int,int] = {}  #git->org
    line_count = 0
    with open(git_spec_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count == 0:
                if row != ['id', 'title', 'content']:
                    print("Row header incorrect for", filename)
                    quit()
                line_count += 1
            else:
                try:
                    org_id:int = titleToOrgID[row[1].strip()]
                    specs_dict[int(row[0])] = org_id
                except KeyError:
                    print("Error: Spec Key is missing: ", row[1])
                    quit()
                line_count += 1
    return specs_dict

def convertSuggestedSpecToOrgID(git_sugg_file:str, issue, spec) -> list[list[int]]:
    """ Converts the specification ids in each row to Original Dataset IDs.
    :param git_sugg_file: Path to the GitRE suggestions CSV
    :param issue: Mapping from generated issue IDs to original issue IDs
    :param spec: Mapping from generated specification IDs to original specifcation IDs
    :return: A two dimensional array representing the CSV with the Original Data IDs for specifications
    """
    suggestions_lst:list[list[int]] = []  #issues->specs
    line_count = 0
    with open(git_sugg_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count == 0:
                if row != ['id', 'specification_id', 'issue_id']:
                    print("Row header incorrect for", filename)
                    quit()
                line_count += 1
            else:
                issue_id = int(row[2])
                specification_id = int(row[1])
                suggestions_lst.append([issue[issue_id], spec[specification_id]])
                line_count += 1

    return suggestions_lst

def getOracleMatches(og_match_file:str) -> list[list[int]]:
    """Load the ground-truth requirement-to-issue links from a CSV file.
    :param og_match_file:  CSV of original matched issue and requirement IDs.
    :returns: List of paired of issue and requirement IDs.
    """
    matches:list[list[int]] = []  #issues->specs
    line_count = 0
    with open(og_match_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            if line_count == 0:
                if row != ['req', 'issue']:
                    print("Row header incorrect for", filename)
                    quit()
                line_count += 1
            else:
                issue_id = int(row[1])
                specification_id = int(row[0])
                matches.append([issue_id, specification_id])
                line_count += 1
    return matches

def calculatePrecisionAndRecall(project_name,results_folder,matches_list:list[list[int]], suggestions_list:list[list[int]]):
    """ Calculates the precision and recall of the generated suggested specifications compared to ground truth suggested specifications
        :param project_name: The name of the project
        :param results_folder: The path to the folder where the results will be stored
        :param matches_list: A two dimensional array where the ground truth suggested specifications are located
        :param suggestions_list: A two dimensional array where the generated suggested specifications are located
        :return: None
    """
    matches_dict = {}
    for key, value in matches_list:
        matches_dict.setdefault(key, []).append(value)
    suggestions_dict = {}
    for key, value in suggestions_list:
        suggestions_dict.setdefault(key, []).append(value)

    #Calculate Recall
    recall_list = [['issue id','req found','total req','recall']]
    recall_avg = []
    for key, m_values in matches_dict.items():
        if key in suggestions_dict:
            s_values = suggestions_dict[key]
            count = 0
            for m in m_values:
                if m in s_values:
                    count += 1
            recall_list.append([key,count,len(m_values),round(count/len(m_values),2)])
            recall_avg.append(count/len(m_values))
        else:
            recall_list.append([key,0,len(m_values),0.0])
            recall_avg.append(0)

    filepath:str = results_folder + '-recall.csv'
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(recall_list)
    
    #Calculate Precision
    precision_list = [['issue id','req found','total req','precision']]
    precision_avg = []
    for key, m_values in matches_dict.items():
        if key in suggestions_dict:
            s_values = suggestions_dict[key]
            count = 0
            for t in s_values:
                if t in m_values:
                    count += 1
            precision_list.append([key,count,len(s_values),round(count/len(s_values),2)])
            precision_avg.append(count/len(s_values))
        else:
            precision_list.append([key,0,0,0.0])
            precision_avg.append(0)

    filepath:str = results_folder + '-precision.csv'
    with open(filepath, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(precision_list)
    print(project_name, ':\t\tP:', round(statistics.mean(precision_avg),2),'\tR:', round(statistics.mean(recall_avg),2))

# Not used in result; instead, used to validate the algorithm.
def catchMissingIssues(results_folder,issues,matches):
    """Write the IDs of original issues absent from the ground truth. Creates a -missing-issues.csv file only when at
    least one mapped issue has no entry in matches

    :param results_folder: Output path for the missing-issues file
    :param issues: Mapping whose values are original issue IDs
    :param matches: Ground-truth issue and requirement pairs
    :returns: None
    """
    missing_issues = []
    for val in issues.values():
        found = False
        for l in matches:
            if val == l[0]:
                found = True
                break
        if not(found):
            missing_issues.append([val])
    if len(missing_issues) > 0:
        filepath:str = results_folder + '-missing-issues.csv'
        with open(filepath, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(missing_issues)


def main():
    K3 = False
    Claude = False
    print("K3 =", K3)
    for project_name in ['blit','cctns','gammaj','keepass','peering','spacefractions','warc']:
        og_issue_file = 'dataset/org/' + project_name + '-og-issues.csv'
        og_req_file = 'dataset/org/' + project_name + '-og-reqs.csv'
        og_match_file = 'dataset/matches/' + project_name + '-og-matches.csv'

        if K3: 
            if Claude:
                out_folder = 'claude-k3-output/'
                results_folder = 'results-K3-claude/' + project_name
            else:
                out_folder = 'gitRE-k3-output/'
                results_folder = 'results-K3/' + project_name
        else:
            out_folder = 'gitRE-alpha-output/'
            results_folder = 'results-alpha/' + project_name        
        git_issue_file = out_folder + project_name + '-git-issues.csv'
        git_spec_file = out_folder + project_name + '-git-specs.csv'
        git_sugg_file = out_folder + project_name + '-git-sugg.csv'
            
        issues_dict = createIssueIDMapping(og_issue_file, git_issue_file)
        specs_dict = createSpecificationIDMapping(og_req_file,git_spec_file)
        gitRE_suggestions = convertSuggestedSpecToOrgID(git_sugg_file, issues_dict, specs_dict)
        matches = getOracleMatches(og_match_file)
        calculatePrecisionAndRecall(project_name,results_folder,matches,gitRE_suggestions)
        catchMissingIssues(results_folder,issues_dict,matches)


if __name__ == "__main__":
    main()
