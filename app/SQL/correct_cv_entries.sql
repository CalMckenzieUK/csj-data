        update all_time_ad_qualities
        left join all_time_listings on all_time_ad_qualities.uid = all_time_listings.uid
        set cv = 1 
        where LOWER(full_ad_text) like '%cv%'
        and cv = 0;