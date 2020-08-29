import os
emily_dict = {
        'https://docs.google.com/spreadsheets/u/1/d/e/2PACX-1vTH8dUIbfnt3X52TrY3dEHQCAm60e5nqo0Rn1rNCf15dPGeXxM9QN9UdxUfEjxwvfTKzbCbZxJMdR7X/pubhtml': [
            0, 0, 0, 0, '']
    }
emily_base_directory = '/Users/joefish/Desktop/state_webscraping/webscraping_validation/emily_files/'
emily_state_list = [
        'AL',
        'AZ',
        'AK',
        'CA',
        'HI',
        'FL',
        'ID',
        'IA',
        'IN',
        'IL',
        'KS',
        'LA',
        'SC',
        'TX',
        'Unclear'
    ]
emily_download_path = os.path.join(emily_base_directory + 'all_files/')

state_url_dict = {
    'https://judicial.alabama.gov/Announcement/COVID_19': [3,1,2,2, "AL_supreme_court"], # looks good
    'https://www.alacourt.gov/COVID19.aspx': [0,0,0,0,'AL_supreme_court'], # looks good
     'https://governor.alabama.gov/newsroom/category/state-of-emergency/': [0,0,0,0,'AL_executive_orders'], # looks good
    'http://www.azcourts.gov/orders/Administrative-Orders-Index/2020-Administrative-Orders': [3,3,2,1, "AZ_supreme_court"],
    'https://azgovernor.gov/executive-orders': [0,0,0,0,'AZ_exec_order'], # looks good
    'https://www.arcourts.gov/arkansas-supreme-court-statement-novel-coronavirus-outbreak-and-courts': [0,0,0,0,'AR_supreme_court'],
    'https://newsroom.courts.ca.gov/news/court-emergency-orders-6794321' : [0,0,0,0,'CA_court'], # looks good
    'https://newsroom.courts.ca.gov/news/judicial-branch-emergency-actions-criminal-civil-and-juvenile-justice': [0,0,0,0,'CA_emergency_orders'], # looks good
    'https://www.manatt.com/insights/newsletters/covid-19-update/covid-19-california-governor-executive-orders': [{'click':['//*[@id="accordion"]/h4[2]']} ,0,0,0,'CA_exec_order'], # looks good
    # 'https://www.courts.state.co.us/announcements/COVID-19.cfm': [0, 0, 0, 0, 'CO_court'], # not scraping
    # 'https://covid19.colorado.gov/covid-19-in-colorado/public-health-executive-orders': [{'click':[
    #     '//*[@id="heading-accordion-8736-1"]/div/a'
    # ]},0,0,0, ' CO_public_health_order'], # # goes to google doc so not scraping
    # 'https://www.colorado.gov/governor/2020-executive-orders': [0,0,0,0,'CO_exec_order'], # goes to google doc so not scraping
    'https://jud.ct.gov/COVID19.htm': [0, 0, 0, 0, 'CT_court'], # looks good
    'https://portal.ct.gov/Office-of-the-Governor/Governors-Actions/Executive-Orders': [0,0,0,0,'CT_exec_order'], # looks good
    'https://courts.delaware.gov/aoc/covid-19': [0, 0, 0, 0, 'DE'],  # not
    'https://www.floridasupremecourt.org/Emergency': [0,0,0,0,'FL_supreme_court'],  # scraping
    'https://www.flgov.com/2020-executive-orders/': [0,0,0,0,'FL_exec_order'], # scraping
    'https://www.courts.state.hi.us/covid-19-information-page#Num3': [0,0,0,0,'HI_supreme_court'],  # scraping
    'https://governor.hawaii.gov/emergency-proclamations/':[0,0,0,0,'HI_exec_order'], # doesnt get orders older than march 31st
    'https://governor.hawaii.gov/executive-orders/': [0,0,0,0,'HI_exec_order'],  # scraping
    'https://isc.idaho.gov/Emergency%20Orders': [0,0,0,0,'ID_court'],  # scraping
    'https://isc.idaho.gov/Superseded': [0,0,0,0,'ID_court'],  # scraping
    'http://www.illinoiscourts.gov/SupremeCourt/Announce/default.asp': [0,0,0,0,'IL_courts'],  # scraping
    'https://www2.illinois.gov/Pages/government/execorders/executive-orders.aspx#y2020': [0,0,0,0,'IL_exec_order'],  # scraping
    'https://www.in.gov/judiciary/3679.htm': [0,0,0,0,'IN_supreme_court'], # scraping
    'https://www.iowacourts.gov/iowa-courts/supreme-court/orders/': [0,0,0,0,'IA_supreme_court'],  # scraping
    'https://coronavirus.iowa.gov/pages/proclamations': [0,0,0,0,'IA_exec_order'],  # scraping
    'https://www.kscourts.org/About-the-Courts/Court-Administration/OJA/Kansas-Courts-Response-to-Coronavirus-(COVID-19)/Administrative-Orders-Related-to-COVID-19':[0,0,0,0,'KS_supreme_court'],  # scraping
    'https://kycourts.gov/Pages/Coronavirus.aspx': [0, 0, 0, 0, 'KY_courts'],   # scraping
    'https://www.lasc.org/COVID19/': [0,0,0,0,'LA_courts'],  # scraping
    'https://www.courts.state.md.us/coronavirusorders': [0, 0, 0, 0, 'MD_supreme_court'],  # scraping
    'https://governor.maryland.gov/covid-19-pandemic-orders-and-guidance/': [0,0,0,0,'MD_exec_order'],  # scraping
    'https://www.courts.maine.gov/covid19.shtml': [0, 0, 0, 0, 'ME'],
    'https://mn.gov/governor/news/executiveorders.jsp': [0,0,0,0,'MN_exec_order'],  # not scraping
    'https://www.sos.ms.gov/content/executiveorders/': [0,0,0,0,'MS_exec_order'],  # scraping
    'https://courts.ms.gov/news/news.php': [0,0,0,0,'MS_supreme_court'],  # scraping but if things are published as "news" it won't get it
    'https://courts.mt.gov': [0,0,0,0,'MT_supreme_court'],  # scraping
    'https://courts.mt.gov/local-virus-rules': [0,0,0,0,'MT_district_court'],  # scraping
    'https://governor.mt.gov/Home/Governor/eo': [0,0,0,0,'MT_exec_order'],  # scraping
    'https://www.governor.nh.gov/news-and-media/emergency-orders-2020': [0,0,0,0,'NH_exec_order'],
    'https://www.courts.state.nh.us/aoc/corona-covid-19.html': [0,0,0,0,'NH_supreme_court'],
    'https://nj.gov/infobank/eo/056murphy/approved/eo_archive.html': [0,0,0,0,'NJ_exec_order'],
    'https://njcourts.gov/public/covid19.html':[0,0,0,0,'NJ_supreme_court'], # does not look like it gets press relesases
    'https://www.governor.state.nm.us/about-the-governor/executive-orders/': [0,0,0,0,'NM_exec_order'],
    'https://www.nmcourts.gov/news.aspx': [0,0,0,0,'NM_supreme_court'],
    'https://nvhealthresponse.nv.gov/news-resources/governor-directives-and-declarations/': [0,0,0,0,'NV_exec_order'],
    'https://www.governor.ny.gov/executive-orders': [0,0,0,0,'NY_exec_order'],
    'https://www.nycourts.gov/latest-AO.shtml': [0,0,0,0,'NY_supreme_court'],
    'https://www.governor.nd.gov/executive-orders': [0,0,0,0,'ND_exec_orders'],
    'http://sc.ohio.gov/coronavirus/default.aspx': [0,0,0,0,'OH_supreme_court'],
    'http://www.pacourts.us/ujs-coronavirus-information': [0,0,0,0,'PA_supreme_court'],
    'https://governor.ri.gov/newsroom/orders/': [0,0,0,0,'RI_exec_order'],
    'https://www.courts.ri.gov/Courts/SupremeCourt/Pages/COVID-19.aspx': [0,0,0,0,'RI_supreme_court'],
    'https://www.utcourts.gov/alerts/': [0,0,0,0,'UT_supreme_court'],
    'https://rules.utah.gov/executive-documents/': [0,0,0,0,'UT_exec_order'],
    'https://www.vermontjudiciary.org/news/information-regarding-coronavirus-disease-2019-covid-19-and-court-operations':[0,0,0,0,'VT_supreme_court'],
    'https://www.sccourts.org/courtOrders/': [0,0,0,0,'SC_supreme_court'],
    'https://www.txcourts.net/orders': [0,0,0,0,'TX'],
    'https://www.governor.wa.gov/office-governor/official-actions/executive-orders': [0,0,0,0,'WA_exec_order'],
    'https://www.governor.wa.gov/office-governor/official-actions/directives': [0,0,0,0,'WA_exec_directive'],
    'http://www.courts.wa.gov/newsinfo/index.cfm?fa=newsinfo.COVID19': [0,0,0,0,'WA_supreme_court'],
    'https://www.courts.state.wy.us/coronavirus-covid-19-updates/': [0,0,0,0,'WY_supreme_court']
}
state_download_path ='/Users/joefish/Desktop/webscraping_output'
state_list = [
        'AL',
        'AZ',
        'AK',
        'CA',
        'HI',
        'FL',
        'ID',
        'IA',
        'IN',
        'IL',
        'KS',
        'LA',
        'SC',
        'TX',
        'Unclear'
    ]
webscraping_output = '/Users/joefish/Desktop/webscraping_output/'
state_directory = '/Users/joefish/Desktop/state_webscraping/'
date = '8_28_2020'
state_regex = '^' + '|'.join(state_list) + '_'
state_file_list = os.listdir(webscraping_output)
emily_file_list = os.listdir(emily_download_path)
new_files = '/Users/joefish/Desktop/state_webscraping/new_files_' + date
all_files = '/Users/joefish/Desktop/state_webscraping/all_files/'
downloaded_links = '/Users/joefish/Desktop/state_webscraping/downloaded_links.txt'
# test changes
