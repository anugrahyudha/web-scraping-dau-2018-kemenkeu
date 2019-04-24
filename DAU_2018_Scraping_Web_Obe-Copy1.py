#!/usr/bin/env python
# coding: utf-8

# # Import libraries

# In[ ]:


import urllib.request # ada juga import urllib.error
from bs4 import BeautifulSoup

import json
import requests
import urllib.request

from lxml import html

from requests import get #beda dengan urllib.request

import pandas as pd

import string
import re

import math

import time
from time import sleep
from random import randint

from IPython.core.display import clear_output

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


#  

# # Simpan Kode Daerah dalam Form Filter

# #### Buka Website yang mau di-Scrape:

# In[ ]:


url = 'http://www.djpk.kemenkeu.go.id/datadasar/'
browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice
browser.get(url) #navigate to the page


# In[ ]:


kode_daerah = []


# In[ ]:


daerah = browser.find_element_by_id('s_daerah')
pilihan = daerah.find_elements_by_tag_name("option")
for pilih in pilihan:
    kode_daerah.append((pilih.get_attribute("value"), pilih.text))


# #### Simpan dalam DataFrame:

# In[ ]:


kode_daerah_df = pd.DataFrame(kode_daerah, columns = ['kode_daerah', 'nama_daerah'])


# #### Cek jumlah:

# In[ ]:


len(kode_daerah_df)


#  

# # Mulai Kumpulkan Data Berdasarkan Daftar Kode Daerah yang Udah Didapatkan

# In[ ]:


url = 'http://www.djpk.kemenkeu.go.id/datadasar/'
browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice
browser.get(url) #navigate to the page


# In[ ]:


dau_2018 = []


# ### Pengumpulan Data:

# In[ ]:


for j in range(0, len(kode_daerah_df)):
    pilih = Select(browser.find_element_by_name('s_daerah'))
    pilih.select_by_value(kode_daerah_df.kode_daerah[j])
    submit_button = browser.find_element_by_xpath("//button[@class = 'form-control btn btn-primary text-uppercase']")
    submit_button.click()
    
    sleep(randint(3,5))
    
    page = BeautifulSoup(browser.page_source, "lxml")
    rows = page.find_all('td', class_ = 'text-right')

    belanja_pegawai_rupiah = rows[0].text
    penduduk_jiwa = rows[1].text
    luas_daratan_km2 = rows[2].text
    luas_lautan_km2 = rows[3].text
    luas_wilayah_km2 = rows[4].text
    ikk = rows[5].text
    ipm = rows[6].text
    pdrb_per_capita_rupiah = rows[7].text
    pad_rupiah = rows[8].text
    dbh_pajak_rupiah = rows[9].text
    dbh_sda_rupiah = rows[10].text
    alokasi_dau_rupiah = rows[11].text   
 
    dau_2018.append((belanja_pegawai_rupiah, penduduk_jiwa, luas_daratan_km2, luas_lautan_km2, luas_wilayah_km2, ikk, ipm,
                     pdrb_per_capita_rupiah, pad_rupiah, dbh_pajak_rupiah, dbh_sda_rupiah, alokasi_dau_rupiah))


# In[ ]:


len(dau_2018)


# ### Melihat Tampilan Data yang Dikumpulkan:

# In[ ]:


dau_2018


# In[ ]:


dau_2018[446]


# In[ ]:


kode_daerah_df.nama_daerah[392]


# #### Menyimpan Data:

# In[ ]:


dau_2018_df = pd.DataFrame(dau_2018, columns = ['Belanja Pegawai (Rupiah)', 'Penduduk (Jiwa)', 'Luas Daratan (km2)',
                                                'Luas Lautan (km2)', 'Luas Wilayah (km2)', 'IKK', 'IPM',
                                                'PDRB/Capita (Rupiah)', 'PAD (Rupiah)', 'DBH Pajak (Rupiah)',
                                                'DBH SDA (Rupiah)', 'Alokasi DAU (Rupiah)'])


# #### Menambahkan Kolom `Nama Daerah`:

# In[ ]:


dau_2018_df['Nama Daerah'] = kode_daerah_df['nama_daerah']


# In[ ]:


print(dau_2018_df)


# #### Menyimpan Data:

# In[ ]:


dau_2018_df.to_csv('dau_2018.csv', index = False)

