## MBFC - a MultiLingual Bug-Fix dataset and its Constructor

The Multi-lingual Bug-Fix dataset Constructor (MBFC) aims to mine bug-fix pairs from public github events, with rich 
information such as bug-fix description, fault type and more.

### Supported Languages and Covered Information (updated 2023.07.20)

| **Language** | **Repo Info** | **Bug-Fix Description** | **Fault Type (partly)** | **File-Level Pair** | **Method-level Pair** | **Line-Level Pair** |
|:------------:|:-------------:|:-----------------------:|:-----------------------:|:-------------------:|:---------------------:|:-------------------:|
| Javascript   | √             | √                       | √                       | √                   | √                     | √                   |
| Python       | √             | √                       | √                       | √                   | √                     | √                   |
| Java         | √             | √                       | √                       | √                   | √                     | √                   |
| C            | √             | √                       | √                       | √                   | √                     | √                   |
| C++          | √             | √                       | √                       | √                   | √                     | √                   |
| C#           | √             | √                       | √                       | √                   | √                     | √                   |
| Go           | √             | √                       | √                       | √                   | going                 | going               |
| PHP          | √             | √                       | √                       | √                   | going                 | going               |
| Rust         | √             | √                       | √                       | √                   | going                 | going               |
| Swift        | √             | √                       | √                       | √                   | going                 | going               |
| Ruby         | √             | √                       | √                       | √                   | going                 | going               |
| TypeScript   | √             | √                       | √                       | √                   | going                 | going               |


### Usage
#### For downloading and preparing new database:
##### (1) Downloads events information of xxxx-xx(year-month):
> python CLI_Command.py --mode download_events --month 2021-01 --downloads_save_dir <your_save_dir>

##### (2) Mine bug-fix commits and get basic information 
> python CLI_Command.py --mode mine_basic_information --au_token <github_au_token> --month_dir <directory to save mined data instances> --downs_save_dir <save_dir_in_step(1)>

##### (3) Infer fault type for mined bugs
> python CLI_Command.py --mode infer_fault_type --month_dir <the path store mined information at (2)> --log_path <log_path>

##### (4) parse method-level and line-level pairs
> python CLI_Command.py --mode parse_contextual_pairs --month_dir <the path store mined information at (2)> --log_path <log_path> --jar_path ./Resource/BFCollector.jar

### Export Data from the database according to your requirements
> python CLI_Command.py --mode export_data --language <which_program_language> --events_type <Push|PR|All> --context_level <File|Method|Line> --fault_type <fault_type_id|All> --output_file <the directory to store satisfied ids and their paths>


### Already Parsed Data (updated 2023.07.20)
#### 2023.07.20 updated
> 2020-1 to 2020-9: <download_link>