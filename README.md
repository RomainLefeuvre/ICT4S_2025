<a id="readme-top"></a>
<br />


<h3 align="center">ICT4S 2025 - Companion repository </h3>

  <p align="center">
    Companion repository of the submitted paper "An Empirical Evaluation of the Energy Profile of
Tasks Managed by Build Automation Tools: The Case of Apache Maven and Gradle"
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#structure">Structure</a>
    </li>
    <li><a href="#Re-run-analysis">Re-run analysis</a></li>
  </ol>
</details>

## Structure

```python
├── analysis               
│   ├── result             # Folder containing the executed notebooks
│   ├── RQ1_NoError_Overall_Tasks_Energy.ipynb
│   ├── RQ1_WithError_Overall_Tasks_Energy.ipynb
│   ├── RQ2_NoError_Gradle_Tasks_Profile.ipynb
│   ├── RQ2_NoError_Maven_Tasks_Profile.ipynb
│   ├── RQ2_WithError_Gradle_Tasks_Profile.ipynb
│   ├── RQ2_WithError_Maven_Tasks_Profile.ipynb
│   ├── RQ3_NoError_GradleDifferentEnergyProfiles.ipynb
│   ├── RQ3_NoError_Maven_Different_Energy_Profiles.ipynb
│   ├── RQ3_WithError_Gradle_Different_Energy_Profiles.ipynb
│   └── RQ3_WithError_Maven_Different_Energy_Profiles.ipynb
├── data                   
│   ├── converted_data     
│   ├── input_data         
│   ├── log                
│   └── output_data        
├── README.md             
├── report.html            # Snake make report
├── requirements.txt       # Python package dependencies for setting up the project environment
├── scripts                # Folder for utility scripts 
└── Snakefile              # SnakeMake workflow file to automate the project's tasks
```

The `analysis` folder contains all the notebooks used for analyzing the research questions:  
>* RQ1. How is the overall energy consumption associated with Maven/Gradle tasks?  
>* RQ2. How is the energy consumption profile by category of Maven/Gradle task?
>   * Overall Energy Consumption by Category
>   * Energy Consumption Profile Per Task and Per Unit of Time

Notebooks in the root of this directory are not executed. The executed notebooks are available in the `result` folder. You can re-run the analysis by executing the workflow.  

For each analysis, two versions are available:  
1. One excluding failed Maven/Gradle tasks (the version used in the paper).  
2. One including failed tasks (see *Section IV – Threats to Validity, C. Construct Validity*).




<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Re-run analysis

1. Create the python virtual environment with required dependencies
   
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ``` 
   (Tested python version : Python 3.11.2)

2. Run the snake make workflow :  

   ```bash
   snakemake --force
   ```
   The workflow execute all the analysis, including the execution of jupyter notebook
       
3. Launch `jupyter notebook`, all the executed notebook are on `analysis/result` folder
  
    ```bash
    jupyter-notebook
    ```
    You can now browse on the executed notebooks
    See files `scripts/regex_maven.py` and `scripts/reges_gradle.py` to
    check the full list of Maven/Gradle plugins/tasks and their corresponding
    category.


4. You can also access the execution report of snakemake through
   ```bash
   snakemake --report report.html
   ```
   The execution logs are located in `.snakemake/log`


<p align="right">(<a href="#readme-top">back to top</a>)</p>


