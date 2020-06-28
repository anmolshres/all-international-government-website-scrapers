if (!($args.Length -eq 1)) {
    Write-Host("Uh-Oh! The number of arguments passed to the script should be 1.")
}
elseif ($args -eq "cdc".ToLower()) {
    scrapy crawl cdc_links
    scrapy crawl cdc_posts -o posts/cdc_posts.json
}
elseif ($args -eq "brazil".ToLower()) {
    scrapy crawl brazil_links
    scrapy crawl brazil_posts -o posts/brazil_posts.json
}
elseif ($args -eq "spain".ToLower()) {
    scrapy crawl spain_links
    scrapy crawl spain_posts -o posts/spain_posts.json
}
elseif ($args -eq "uk".ToLower()) {
    scrapy crawl uk_links
    scrapy crawl uk_posts -o posts/uk_posts.json
}
elseif ($args -eq "italy".ToLower()) {
    scrapy crawl italy_links
    scrapy crawl italy_posts -o posts/italy_posts.json
}
else {
    Write-Host("Uh-Oh! Sorry, that region does not have any script for it. `nCheck README for all available options.")
}