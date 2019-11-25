# extract-sqli

> For forensics and reports purposes, allow you to extract infos and present them, stored in SQLite DataBases

**👨‍🔬 Inspired by:** 

 - SQLite viewer => [https://inloop.github.io/sqlite-viewer/](https://inloop.github.io/sqlite-viewer/)
 - GitHub Repo => [https://github.com/inloop/sqlite-viewer](https://github.com/inloop/sqlite-viewer)

**⚙ Technical choices:**

 - No use of external library (like using template system)
 - HTML/CSS rendered by library hosted on CDN (no hard inclusions)
 - Report is generated on hard-drive to avoid uploading data online : confidentiality and security purposes

**💥 Warnings:**

 - Tests are mostly insignificant
 - Script has been tested on Windows and Linux architecture system

🚀 Future Update:
-
 - Allowing specific request by prompting it ✅ [25/11/2019]
 _ Refactoring html templating
