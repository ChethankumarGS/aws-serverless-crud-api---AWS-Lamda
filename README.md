# Serverless Task Management CRUD API

A production-ready serverless RESTful API backend built on AWS using Python 3.11, AWS Lambda, Amazon API Gateway, and Amazon DynamoDB. Provisions infrastructure as code using the Serverless Framework.

## Architecture

- **Compute:** AWS Lambda (Python 3.11)
- **API Routing:** Amazon API Gateway (REST API with CORS)
- **Database:** Amazon DynamoDB (On-Demand Capacity)
- **Infrastructure as Code:** Serverless Framework (`serverless.yml`)
- **Security:** AWS IAM (Least-Privilege Roles)

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/tasks` | Create a new task |
| `GET` | `/tasks/{id}` | Get a task by Partition Key `taskId` |
| `GET` | `/tasks` | List all tasks |
| `PUT` | `/tasks/{id}` | Update task status or fields |
| `DELETE` | `/tasks/{id}` | Delete task by ID |

## Deployment Instructions

1. **Install Prerequisites:**
   - Node.js & Serverless CLI (`npm install -g serverless`)
   - Python 3.11
   - AWS CLI configured with valid credentials (`aws configure`)

2. **Deploy Stack:**
   ```bash
   sls deploy --stage dev
