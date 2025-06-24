🧰 Log Combiner Tool
A fast, multithreaded Python script that recursively scans folders for web server logs (access, error, ssl) — including .log and .xz compressed files — and combines them by type into a clean, organized output directory.

The .xz extension is commonly used for pre-compressed log files in NGINX environments. During DFIR investigations, these files are often all you have. This tool automatically detects and decompresses .xz files in-memory, letting you immediately parse and combine logs into searchable, readable text files.

You can then index the combined logs into your favorite analysis tool — I recommend Splunk.

📸 Examples

Input — Raw Logs (including .xz):

![image](https://github.com/user-attachments/assets/b8fbd9e0-46ac-4bd4-bc86-08d6f035a3ad)


Output — Clean Combined File:

![image](https://github.com/user-attachments/assets/63cdee57-b418-44b7-9ea6-5b9d001f4c28)


Simple, single file to work with:


✨ FEATURES

🔍 Automatically detects access, error, and ssl logs by filename

📦 Supports both plain .log and compressed .xz files

⚡ Blazing fast with multithreaded processing

🗂️ Preserves original subfolder structure in output

🧑‍💻 Simple interactive CLI — no arguments needed

🧱 No external dependencies — pure Python

📌 Important Behavior – Log Detection Logic

The script matches files based on the presence of keywords in the filename, not strict naming conventions. For example:

Files like access.log, access.log-20250623, broadway_access_20250623.xz will all be treated as access logs

Similarly, any file with error or ssl in its name will be matched accordingly

This flexible matching ensures compatibility with most rotated or archived log naming schemes.

📂 EXAMPLE STRUCTURE

Input Directory (/logs):
/logs
├── site1
│   ├── access.log
│   ├── error.log
│   ├── access.log-20250623.xz
│   └── access.log-20250624.xz
├── site2
│   ├── ssl.log
│   └── error.log

Output Directory (/combined_logs):

/combined_logs
├── site1
│   ├── combined-access.log
│   ├── combined-error.log
├── site2
│   ├── combined-ssl.log
│   ├── combined-error.log
🚀 HOW TO USE

Run the script:
python NGINX_Parser.py

When prompted:

Enter the input directory containing your logs
Enter the output directory for the combined logs
Done! The tool will process and combine your logs by type into the output directory.

🛠️ HOW IT WORKS

📛 File names are scanned for keywords:

"access" → Access logs
"error" → Error logs
"ssl" → SSL logs

🧩 .xz files are extracted in-memory using Python’s built-in lzma module

📝 All matched files are grouped by type and written into:

combined-access.log
combined-error.log
combined-ssl.log

🧪 REQUIREMENTS

Python 3.7 or newer

No additional dependencies (100% standard library)

📄 LICENSE

This project is licensed under the MIT License.

👨‍💻 Developed by Jacob Wilson – [https://dfirvault.com](https://dfirvault.com)

💬 Feedback, forks, and pull requests are always welcome!


