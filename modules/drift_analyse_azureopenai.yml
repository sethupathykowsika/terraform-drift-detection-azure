import os
import requests
from openai import AzureOpenAI

# -----------------------------------------
# 🔍 Test Azure OpenAI endpoint connectivity
# -----------------------------------------
try:
    test_url = os.getenv("AZURE_OPENAI_API_BASE").rstrip("/") + "/openai/deployments?api-version=2023-07-01-preview"
    test_headers = {
        "api-key": os.getenv("AZURE_OPENAI_API_KEY")
    }
    test_response = requests.get(test_url, headers=test_headers)
    print(f"[DEBUG] Connection Test Status Code: {test_response.status_code}")
    print(f"[DEBUG] Connection Test Response: {test_response.text}")
except Exception as conn_err:
    print(f"[ERROR] Connection test failed: {conn_err}")
    exit(1)

# -----------------------------------------
# ✅ Initialize Azure OpenAI Client
# -----------------------------------------
client = AzureOpenAI(
    azure_endpoint=os.getenv("AZURE_OPENAI_API_BASE"),  # Azure OpenAI endpoint
    api_version="2024-12-01-preview",
    api_key=os.getenv("AZURE_OPENAI_API_KEY")
)

# -----------------------------------------
# 📄 Read the Terraform drift report file
# -----------------------------------------
app_folder = os.getenv("APP_FOLDER")
drift_report_file = os.getenv("DRIFT_REPORT_FILE")

try:
    with open(f"{app_folder}/{drift_report_file}", "r") as file:
        terraform_plan_text = file.read()
except FileNotFoundError:
    print(f"[ERROR] File not found: {app_folder}/{drift_report_file}")
    exit(1)

# -----------------------------------------
# 🧠 Build the prompt for the AI model
# -----------------------------------------
prompt = f"""
You are a Terraform expert reviewing the output of a Terraform plan. Your task is to extract and summarize infrastructure **drift**, which refers to differences between the current live Azure environment and what is defined in the Terraform configuration.

Please clearly identify and report the following types of changes:

1. **Created (`+`)** – Resources that are defined in Terraform but missing in Azure, and will be created.
2. **Updated (`~`)** – Resources that still exist but have configuration differences compared to Terraform (e.g., networking, access rules).
3. **Deleted (`-`)** – Resources that have been manually deleted in Azure, but still exist in the Terraform state file.
4. **Replaced (`-/+`)** – Resources that will be destroyed and recreated due to core attribute changes.

  Do NOT include:
- Tag-only changes
- Metadata changes that do not affect actual infrastructure behavior

For each identified drifted resource, provide the following details:
- **Resource type and name** (e.g., `azurerm_storage_account.stg`)
- Include resource name
- **Type of change**: Create, Update, Delete, or Replace
- A short **summary of key configuration differences** (before and after state)
- If applicable, mention:
    - "Manually deleted in Azure but still present in Terraform state"
    - "Configuration manually changed in Azure"

Ensure the explanation is simple and clear enough for a non-technical audience to understand the significance of the drift.

Here is the Terraform plan output to analyze:
{terraform_plan_text}
"""

# -----------------------------------------
# 🧠 Call Azure OpenAI to analyze drift
# -----------------------------------------
try:
    response = client.chat.completions.create(
        model="Driftdetectormodel",  # Make sure this matches your Azure OpenAI deployment name
        messages=[
            {"role": "system", "content": "You are an AI that processes Terraform plans."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000,
        temperature=0.2
    )

    filtered_result = response.model_dump()['choices'][0]['message']['content'].strip()

    # 💾 Save the processed result
    filtered_drift_report_file = os.getenv("FILTERED_DRIFT_REPORT_FILE")
    with open(f"{app_folder}/{filtered_drift_report_file}", "w") as filtered_file:
        filtered_file.write(filtered_result)

    print(filtered_result)
    print("Filtered drift report (without tags) has been successfully generated.")

except Exception as e:
    print(f"[ERROR] An unexpected error occurred during OpenAI call: {e}")
    exit(1)

    


# import openai
# import os

# # Use OpenAI API key from environment variable
# openai.api_key = os.getenv("OPENAI_API_KEY")

# # Use new v1 client
# client = openai.OpenAI(api_key=openai.api_key)

# # File paths from environment
# app_folder = os.getenv("APP_FOLDER", ".")
# drift_report_file = os.getenv("DRIFT_REPORT_FILE", "drift_output.txt")
# filtered_drift_report_file = os.getenv("FILTERED_DRIFT_REPORT_FILE", "filtered_drift_output.txt")

# # Read drift report
# try:
#     with open(f"{app_folder}/{drift_report_file}", "r") as file:
#         terraform_plan_text = file.read()
# except FileNotFoundError:
#     print(f"Error: The file '{drift_report_file}' was not found in '{app_folder}'.")
#     exit(1)

# # Prompt construction
# prompt = f"""
# You are a Terraform expert reviewing the output of a Terraform plan. I need you to extract all the infrastructure changes from the plan, including the resources affected, along with their pre- and post-apply states. Please exclude any tag changes.

# Terraform Plan:
# {terraform_plan_text}
# """

# # Call OpenAI ChatCompletion API using v1 client
# try:
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are an AI that processes Terraform plans."},
#             {"role": "user", "content": prompt}
#         ],
#         max_tokens=2000,
#         temperature=0.2
#     )

#     filtered_result = response.choices[0].message.content.strip()

#     # Save the output
#     with open(f"{app_folder}/{filtered_drift_report_file}", "w") as filtered_file:
#         filtered_file.write(filtered_result)

#     print(filtered_result)
#     print("✅ Filtered drift report (excluding tags) successfully generated.")

# except Exception as e:
#     print(f"❌ An error occurred: {e}")
#     exit(1)
