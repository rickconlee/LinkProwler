# What Is LinkProwler? 

LinkProwler is a tool written in Python that is used to scan a target website for links. LinkProwler will scan all links on a target site website using Selenium Webdriver (image downloaded separately), then store that data in a JSON file that you can digest later. 

Docker Hub repo can be found here: https://hub.docker.com/repository/docker/actionspec/linkprowler
or run `$ docker pull actionspec/linkprowler:[tag]`

# Usage 

## Standalone container: 

```
$ docker run -e SELENIUM_URL=http://<HOST OR IP OF SELENIUM INSTANCE>:PORT -e TARGET_URL=https://example.com/ -v /local/directory/path:/usr/src/app/crawls actionspec/linkprowler:TAG
```
### LinkProwler output

The output from the program will bein JSON format. Each run will create a unique file. Below is a crawl that was executed against `https://actionspec.com`

```
{
    "Internal URLs": [
        "mailto://team@actionspec.com",
        "https://actionspec.com/tags/devops",
        "https://actionspec.com/services/learn-more",
        "https://actionspec.com/tags/jpg-to-webp",
        "https://actionspec.com/blog/environmentally-friendly-devops-focused-hosting-companies/",
        "https://actionspec.com/tags/web-servers",
        "https://actionspec.com/tags/hugo",
        "https://actionspec.com/blog/3-tips-for-devops-success/",
        "https://actionspec.com/services/devops-staff-augmentation/",
        "https://actionspec.com/notice/notice-1/",
        "https://actionspec.com/categories/server-software",
        "https://actionspec.com/tags/cms",
        "https://actionspec.com/blog/should-i-use-apache-or-nginx/",
        "https://actionspec.com/blog/",
        "https://actionspec.com/blog/page/2/",
        "https://actionspec.com/contact",
        "https://actionspec.com/",
        "https://actionspec.com/blog/3-things-to-know-about-wordpress-and-devops/",
        "https://actionspec.com/services/managed-devops-hosting/",
        "https://actionspec.com/about",
        "https://actionspec.com/tags/speed",
        "https://actionspec.com/services",
        "https://actionspec.com/categories/cloud-hosting",
        "https://actionspec.com/tags/python",
        "https://actionspec.com/blog",
        "https://actionspec.com/blog/make-wordpress-fast/",
        "https://actionspec.com/blog/convert-image-to-webp-python/",
        "https://actionspec.com/tech",
        "https://actionspec.com/tags/apache",
        "https://actionspec.com/tags/business-process",
        "https://actionspec.com/tags/digital-ocean",
        "https://actionspec.com/blog/what-is-a-headless-cms/",
        "https://actionspec.com/services/vcio-services/",
        "https://actionspec.com/tags/a2-hosting",
        "https://actionspec.com/categories/devops-practices",
        "https://actionspec.com/notice/notice-2/",
        "https://actionspec.com/tags/nginx",
        "https://actionspec.com/tags/jamstack",
        "https://actionspec.com/author/actionspec",
        "https://actionspec.com/services/managed-devops/",
        "https://actionspec.com/tags/google",
        "https://actionspec.com/blog/5-reasons-we-left-wordpress-in-2021/",
        "https://actionspec.com/tags/wordpress",
        "https://actionspec.com/tags/scripts",
        "https://actionspec.com/categories/digital-transformation",
        "https://actionspec.com/categories/tech-tips",
        "https://actionspec.com/tags/green-hosting"
    ],
    "External URLs": [
        "https://www.linkedin.com/company/actionspec",
        "https://twitter.com/actionspec",
        "https://github.com/actionspec"
    ]
}
```

## Using Compose 

TODO - the startup order needs a little work, and we need to add a graceful exit. That being said, you can use this docker-compose template to run it. Once the link crawler is complete, you can hit `CTRL-C` to kill it. replace the variables below for your targeted run, save it, then run `docker-compose up`

```
version: "3.9"
services:
  selenium:
    image: "selenium/standalone-chrome:91.0.4472.114-chromedriver-91.0.4472.101"
  linkprowler:
    image: "actionspec/linkprowler:[TAG]"
    restart: on-failure
    volumes:
      - [/local/directory/for/results]:/usr/src/app/crawls
    environment:
      SELENIUM_URL: "http://selenium:4444"
      TARGET_URL: "http://example.com"
    depends_on:
      - "selenium"
```