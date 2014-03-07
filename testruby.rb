#!/usr/bin/env ruby

#Needed to get the html page with the forum topics
require 'rubygems'
require 'nokogiri'
require 'open-uri'

#URL for the forum
flyertalk_url = 'http://www.flyertalk.com/forum/mileage-run-deals-372/'

#Array of airline two letter codes to match against
airlines = ["DL" , "AS" , "KL" , "AF"]

#Array of airport codes to match against
airports = ["BWI" , "DCA" , "IAD" , "JFK" , "BOS" , "SEA" , "SFO" , "SJC" , "OAK"]

#Grab the page
page = Nokogiri::HTML(open(flyertalk_url))

#Grab the links from the forum
links = page.css('table tbody tr a')

#Clean out the non-thread title data and convert to thread array
threads = links.map { |link| link.text.strip }

#Clear out the non matching airlines and cities via grep and regex
threads = threads.grep(/^#{airlines.join('|^')}/).grep(/#{airports.join('|')}/)

puts threads

