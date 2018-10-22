# ScrapeFBGroupMembers

Tool to scrape details: Name and Profile link of members of a particular group.
The locators(xpath) are likely to change. 
Need to update the loop count according to the numbers of members. Here, the loop count is for group with about 200k members. 

## Requirements:
```
pip install selenium
pip install xlwt
```

## Command to run:
```
python scrape_data.py {FbUsername} {FbPassword} {FbGroupID}
```
