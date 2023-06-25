# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource            | Service Tier     | Monthly Cost        | 
| ------------              | ------------     | ------------        |
| *Azure Postgres Database* | Standard_D2ds_v4 | USD 144.66          |
| *Azure Service Bus*       | Standard         | 10 USD/12.5 MILLION |
| Azure Function App        | Y1               | Free                |
| Azure Service App Plan    | Standard S1      | USD 69.35           |

## Architecture Explanation
This is a placeholder section where you can provide an explanation and reasoning for your architecture selection for both the Azure Web App and Azure Function.

# Azure Web App Architecture

For the Azure Web App, we have chosen the following architecture to ensure cost-effectiveness:

- App Service Plan: We have selected the F1 tier for our web app. This plan offers a cost-effective solution for low-traffic applications. Since our application is not expected to have high user load at peak, the F1 tier provides sufficient resources while keeping the costs low.

By choosing the F1 tier, we can take advantage of the free tier benefits provided by Azure, which includes 60 minutes of CPU time per day and 1 GB of storage. This helps us minimize the cost while still meeting the requirements of our application.

## Azure Function Architecture

For the Azure Function, we have chosen the following architecture to ensure cost-effectiveness:

- App Service Plan: We have selected the Consumption Plan for our Azure Function. This plan offers a cost-effective solution as we only pay for the actual execution time of the function.

Since our function is triggered by messages in the service bus queue and is not expected to run continuously, the Consumption Plan allows us to scale automatically based on the incoming workload. This eliminates the need for provisioning and managing dedicated resources, resulting in cost savings.

## Shared App Service Plan

To further optimize costs, we have decided to share the same App Service Plan between the web app and the Azure Function. By doing so, we can reduce the cost associated with multiple service plans and efficiently utilize the available resources.

By carefully selecting the appropriate App Service Plans for both the web app and the Azure Function, we have designed an architecture that meets our application's requirements while keeping the costs under control.
