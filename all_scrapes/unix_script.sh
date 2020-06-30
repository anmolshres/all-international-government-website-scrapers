if [ $# != 1 ]; then
    printf "Uh-Oh! The number of arguments passed to the script should be 1.\n"
elif [ "${1,,}" == "cdc" ]; then
    scrapy crawl cdc_links
    scrapy crawl cdc_posts -o posts/cdc_posts.json
elif [ "${1,,}" == "brazil" ]; then
    scrapy crawl brazil_links
    scrapy crawl brazil_posts -o posts/brazil_posts.json
elif [ "${1,,}" == "spain" ]; then
    scrapy crawl spain_links
    scrapy crawl spain_posts -o posts/spain_posts.json
elif [ "${1,,}" == "uk" ]; then
    scrapy crawl uk_links
    scrapy crawl uk_posts -o posts/uk_posts.json
elif [ "${1,,}" == "italy" ]; then
    scrapy crawl italy_links
    scrapy crawl italy_posts -o posts/italy_posts.json
elif [ "${1,,}" == "germany" ]; then
    scrapy crawl germany_links
    scrapy crawl germany_posts -o posts/germany_posts.json
elif [ "${1,,}" == "peru" ]; then
    scrapy crawl peru_links
    scrapy crawl peru_posts -o posts/peru_posts.json
elif [ "${1,,}" == "all" ]; then
    bash unix_script.sh cdc
    bash unix_script.sh brazil
    bash unix_script.sh spain
    bash unix_script.sh uk
    bash unix_script.sh italy
    bash unix_script.sh germany
    bash unix_script.sh peru
else
    printf "Uh-Oh! Sorry, that region does not have any script for it. \nCheck README for all available options.\n"
fi
