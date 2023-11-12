import json
from github import Github
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from prompts.prompts import test_prompt
import re
import os
load_dotenv()


PATTERN = r'<!--(.*?)-->'
gpt4 = ChatOpenAI(temperature=0, model="gpt-4")
test_chain = LLMChain(llm=gpt4, prompt=test_prompt)

def find_pattern_in_text(text, pattern):
    matches = re.findall(pattern, text, re.DOTALL)
    return matches

def build_map(repo, path="", map={}):
    contents = repo.get_contents(path)
    for content in contents:
        if content.type == "dir":
            build_map(repo, content.path, map)
        elif content.type == "file":
            file_content = content.decoded_content.decode("utf-8")
            matches = find_pattern_in_text(file_content, PATTERN)
            for match in matches:
                print(f"Match found in {content.path}:")
                map[match.strip()] = content.path
    return map
                
g = Github(os.getenv('GH_TOKEN'))

owner = "Prompty-Developers"

repo_name = os.getenv('TEST_REPO')
docs_name = os.getenv('DOCS_REPO')

full_repo = f"{owner}/{repo_name}"
docs_repo = f"{owner}/{docs_name}"
pr = 583
repo = g.get_repo(full_repo)
docs_repo = g.get_repo(docs_repo)

pull_request = repo.get_pull(pr)
files_changed = pull_request.get_files()


with open("map.json", "r") as json_file:
    map = json.loads(json_file.read())

for file in files_changed:
    file_name = f"{repo_name}/{file.filename}"
    if file_name in map:
        current_doc = docs_repo.get_contents(map[file_name]).decoded_content.decode("utf-8")
        # TODO: handle documentation update
    else:
        with open("template.md", "r") as json_file:
            template = json_file.read()
        
        contents = repo.get_contents(file.filename)
        contents = contents.decoded_content.decode()
    
        test_chain = LLMChain(llm=gpt4, prompt=test_prompt)
        result = test_chain.run({
            "contents": contents,
            "template": template
        })
        print(result)

        # with open("test.md", "w") as file:
        #     file.write(result)
        

    break
    

    
