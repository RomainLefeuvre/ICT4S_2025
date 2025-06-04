import glob

# Get all notebook names from the 'analysis' directory dynamically
notebooks = [f.split('/')[-1].replace('.ipynb', '') for f in glob.glob("analysis/*.ipynb")]

# Define the 'rule all' to collect all results dynamically using the 'notebooks' list
rule all:
    input:
        expand("analysis/result/{notebook}.ipynb", notebook=notebooks),
        "data/output_data/overview_daylight_witherror.csv",
        "data/output_data/overview_daylight_noerror.csv",
        "data/output_data/all_tasks_witherror.csv",
        "data/output_data/all_tasks_noerror.csv",
# Define the 'exec_notebook' rule to process each notebook

rule generate_csv_with_error:
    input:
        script="scripts/overview.py",
        input_dir="data/converted_data",
        loc_dir="data/input_data/cloc_reports"
    output:
        overview="data/output_data/overview_daylight_witherror.csv",
        all_task="data/output_data/all_tasks_witherror.csv",
        log="data/log/log_daylight_witherror.txt"
    shell:
        "python {input.script} {input.input_dir} {input.loc_dir} data/output_data overview_daylight.csv False > {output.log}"

rule generate_csv_no_error:
    input:
        script="scripts/overview.py",
        input_dir="data/converted_data",
        loc_dir="data/input_data/cloc_reports"
    output:
        overview="data/output_data/overview_daylight_noerror.csv",
        all_task="data/output_data/all_tasks_noerror.csv",
        log="data/log/log_daylight_noerror.txt"
    shell:
        "python {input.script} {input.input_dir} {input.loc_dir} data/output_data overview_daylight.csv True > {output.log}"


rule exec_notebook:
    input:
        notebook="analysis/{notebook}.ipynb",
        overview_daylight_noerror="data/output_data/overview_daylight_noerror.csv",
        all_tasks_noerror="data/output_data/all_tasks_noerror.csv",
        overview_daylight_witherror="data/output_data/overview_daylight_witherror.csv",
        all_tasks_witherror="data/output_data/all_tasks_witherror.csv",

    output:
        "analysis/result/{notebook}.ipynb"
    log:
        ".snakemake/log/{notebook}.log"  # Log file for each notebook
    shell:
        """
        
        echo "Starting execution of {input.notebook} to {output}" > {log}  # Write initial log message
        jupyter nbconvert --to notebook --execute {input.notebook} --output 'result/{wildcards.notebook}.ipynb' >> {log} 2>&1
        echo "Finished execution of {input.notebook}" >> {log}  # Write final log message
        """