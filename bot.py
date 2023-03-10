import discord
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import asyncio
import os
import traceback
from discord.ext import commands
from discord.utils import get


TOKEN = os.environ['DISCORD_TOKEN']
GUILD = os.environ['DISCORD_GUILD']
JOYCES_USERNAME = os.environ['JOYCES_USERNAME']
JOYCES_PASSWORD = os.environ['JOYCES_PASSWORD']

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='-', intents=intents)

async def scrape():
    print("Searching...")
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    chromedriver = "./chromedriver"
    driver = webdriver.Chrome(service = Service(chromedriver), options=chrome_options)
    await asyncio.sleep(10)
    # chromedriver = ChromeDriverManager().install()

    # driver = webdriver.Chrome(chromedriver)
    try:
        driver.get('https://www.tds.ms/CentralizeSP/Student/Login/joycesdrivingschool')
    except (TimeoutException) as e:
        retries = 10
        if retries > 0:
            retries -= 1
            print("Retries left, " + retries + " Continuing on".format(retries, traceback.format_exc()))
            await asyncio.sleep(5)
        else:
            raise e


    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))

    username = driver.find_element(By.XPATH, '//*[@id="username"]')
    username.send_keys(JOYCES_USERNAME)

    password = driver.find_element(By.XPATH, '//*[@id="password"]')
    password.send_keys(JOYCES_PASSWORD)

    WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[3]/form[1]/div[6]/button'))).click()

    driver.get('https://www.tds.ms/CentralizeSP/BtwScheduling/Lessons?SchedulingTypeId=1')

    tbody2 = driver.find_element(By.XPATH, '//*[@id="datepicker"]/div/div[2]/table/tbody')
    elements2 = tbody2.find_elements(By.CLASS_NAME, 'ui-state-available')

    tbody = driver.find_element(By.XPATH, '//*[@id="datepicker"]/div/div[1]/table/tbody')
    elements = tbody.find_elements(By.CLASS_NAME, 'ui-state-available')

    oldelements = elements + elements2
    
    driver.quit()

    return oldelements


async def main(ctx, oldelements):
    origlen = len(oldelements)

    oldelements = asyncio.run(scrape())


    output = "Joyce's BTW Available! (" + str(len(oldelements)) + ")"
    guild = discord.utils.get(bot.guilds, name=GUILD)

    searched_role = get(guild.roles, name='Joyces')

    print("Found " + str(len(oldelements)))

    if (len(oldelements) > 0 and len(oldelements) != origlen):
        await ctx.send(output)
        await ctx.send(searched_role.mention)

    return oldelements

@bot.command(name='start')
@commands.is_owner()
async def start(ctx):
    oldelements = []
    await ctx.send('Starting program...')

    while (True):
        oldelements = await main(ctx, oldelements)

        await asyncio.sleep(300)

@bot.command(name = 'available')
async def available(ctx):
    await ctx.send("Searching...")
    await ctx.send("Found " + str(len(asyncio.run(scrape()))) + ".")

@bot.command(name= 'end')
@commands.is_owner()
async def end(ctx):
    print("Manually ended program.")
    await ctx.send('Ending program...')
    exit()

bot.run(TOKEN)
