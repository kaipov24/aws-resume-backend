# AWS Serverless Resume Website

A static resume website deployed on AWS with a live visitor counter.

## Architecture
- S3 + CloudFront — static hosting (HTTPS)
- API Gateway + Lambda (Python) — backend API
- DynamoDB — persistent visitor storage
- Terraform — Infrastructure as Code
- GitHub Actions — CI/CD for both frontend and backend

### Live site
👉 [https://dra84ptxmq6m.cloudfront.net/](https://dra84ptxmq6m.cloudfront.net/)
