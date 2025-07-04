import os
import sys
from datetime import datetime

def create_summary(paper_path):
    paper_name = os.path.splitext(os.path.basename(paper_path))[0]
    date_str = datetime.now().strftime("%Y-%m-%d")
    post_path = f"_posts/{date_str}-{paper_name}.markdown"

    with open(post_path, "w") as f:
        f.write(f"""---
layout: tabbed_post
title:  \"{paper_name}\"
date:   {datetime.now().strftime('%Y-%m-%d %H:%M:%S +0200')}
categories: ai forskning
---

## For Barn

Her kommer en oppsummering for barn av \"{paper_name}\".

## For Videregåendeelever

Her kommer en oppsummering for videregåendeelever av \"{paper_name}\".

## For Universitets- og Høyskolenivå

Her kommer en oppsummering for universitets- og høyskolenivå av \"{paper_name}\".
""")

if __name__ == "__main__":
    paper_path = sys.argv[1]
    create_summary(paper_path)