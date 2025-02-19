# Terraform Managed, AWS Hosted Resume

![System Design](/AWS.drawio.png)

While I'm #OpenToWork, I like to stay sharp with both established and new technologies. Recently, I deployed my resume to an AWS cloud infrastructure using AWS technologies such as Lambda, DynamoDB, S3, and API Gateway - all orchestrated with Terraform IaC.

### Overview of Steps Taken:

1. Established secure access with AWS IAM with a root account, an organization, user accounts with 2FA, and policies/groups adhering to Principle of Least Privilege.
2. Translated my resume to HTML and CSS (no frameworks!).
3. Created an AWS S3 bucket for static webpage hosting.
4. Used AWS CloudFront for CDN and HTTPS.
5. Obtained a domain through AWS Route53 and configured DNS records including the www subdomain.
6. Created a DynamoDB table to store visitor counts in a table where the page URI is the key and the value is the count.
7. Authored a Python Lambda function to retrieve and increment the page visitor count, complete with unit tests.
8. Publicized the Lambda function through AWS API Gateway with a POST Rest endpoint.
9. Using Javascript, added an asynchronous method to query the POST endpoint for visitor count and display on the resume webpage.
10. Using GitHub Actions, created a CI/CD deployment pipeline to sync the AWS S3 bucket triggered with updated files from the code repo main branch.
11. Using the Infrastructure as Code (IaC) platform Terraform, created a deployment blueprint for cloud infrastructure such as the Lambda functions.

I’m passionate about building secure, scalable, and efficient systems, and I’m excited to bring this energy to your team. If you’re looking for a dedicated software engineer who loves solving problems and learning new technologies, let’s connect!

📩 Feel free to reach out if you have any opportunities or just want to chat about tech!
