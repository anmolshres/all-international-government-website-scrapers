if (!($args.Length -eq 1)) {
    Write-Host("Uh-Oh! The number of arguments passed to the scrpt should be 1.")
}
elseif ($args -eq "cdc".ToLower()) {
    scrapy crawl cdc_links
    scrapy crawl cdc_posts -o posts/cdc_posts.json
}
else {
    Write-Host("Uh-Oh! Sorry, that region does not have any script for it. `nCheck README for all available options.")
}