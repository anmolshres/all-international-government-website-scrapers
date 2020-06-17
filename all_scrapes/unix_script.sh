if [ $# != 1 ]; then
    printf "Uh-Oh! The number of arguments passed to the script should be 1.\n"
elif [ "${1,,}" == "cdc" ]; then
    scrapy crawl cdc_links
    scrapy crawl cdc_posts -o posts/cdc_posts.json
else
    printf "Uh-Oh! Sorry, that region does not have any script for it. \nCheck README for all available options.\n"
fi
