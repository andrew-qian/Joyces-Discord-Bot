import discord
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import os
from discord.ext import commands
from discord.utils import get

TOKEN = os.environ['DISCORD_TOKEN']
GUILD = os.environ['DISCORD_GUILD']

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='-', intents=intents)

async def main(ctx, oldelements):
    origlen = len(oldelements)
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless=new')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("window-size=1920,1080")

    chromedriver = "./chromedriver"
    driver = webdriver.Chrome(service = Service(chromedriver), options=chrome_options)
    # chromedriver = ChromeDriverManager().install()

    # driver = webdriver.Chrome(chromedriver)
    driver.minimize_window()

    url = 'https://www.tds.ms/CentralizeSP/Student/Login/joycesdrivingschool'
    driver.get(url)

    username = driver.find_element(By.XPATH, '//*[@id="username"]')
    username.send_keys('Qia12779')

    password = driver.find_element(By.XPATH, '//*[@id="password"]')
    password.send_keys('9418123')

    sign_in = driver.find_element(By.XPATH, '/html/body/div[3]/form[1]/div[6]/button')
    sign_in.click()

    driver.get('https://www.tds.ms/CentralizeSP/BtwScheduling/Lessons?SchedulingTypeId=1')

    tbody2 = driver.find_element(By.XPATH, '//*[@id="datepicker"]/div/div[2]/table/tbody')
    elements2 = tbody2.find_elements(By.CLASS_NAME, 'ui-state-available')

    tbody = driver.find_element(By.XPATH, '//*[@id="datepicker"]/div/div[1]/table/tbody')
    elements = tbody.find_elements(By.CLASS_NAME, 'ui-state-available')

    output = "Joyce's BTW Available! (" + str(len(elements) + len(elements2)) + ")"
    guild = discord.utils.get(bot.guilds, name=GUILD)

    oldelements = elements + elements2

    newlen = len(oldelements)

    searched_role = get(guild.roles, name='Joyces')

    if (len(elements) + len(elements2) > 0 and newlen != origlen):
        await ctx.send(output)
        await ctx.send(searched_role.mention)

    return oldelements



@bot.command(name='start')
async def start(ctx):
    oldelements = []
    await ctx.send('Starting program...')

    while (True):
        oldelements = await main(ctx, oldelements)

        time.sleep(300)

@bot.command(name='fuckyougrad')
async def fuckyougrad(ctx):
    await ctx.send('fuck you grad') #fix later

@bot.command(name= 'end')
async def end(ctx):
    if ctx.message.author.id =='380112064401899520':
        await ctx.send('Ending program...')
        await ctx.bot.logout()

bot.run(TOKEN)