import pyautogui
import subprocess
import time

text = "This is where, AI is going to go. So right now we are in the age of Generative A.I.\nSo generative A.I is Chat G.P.T, Midjourney, you're generating music, art, text.\nWe're coming to agentic A.I. Agentic A.I is A.I that can actually think like an employee.\nIt can solve complex problems without human intervention.\nSo you can go to your Agentic A.I and you will soon be able to say, listen, I run a real estate property company,\nI need a really interesting post to showcase my newest development.\nThe A.I will go analyze all the pictures in your Google Drive, pick the best pictures\nwhich are gonna create the best response, write a caption and come up with three different ideas,\npost three different ideas on TikTok, analyze, the data, generate the video, generate the voice, generate everything.\nAnd then see which one has the best response, and then turn that into a Facebook ad,\nput that ad on Facebook, tap into your credit card account,\ngo and deploy money to Meta, to pay for the ad,\nanalyze results of the ad, decide if it should kill it, expand it, tweak it, optimize it,\nthen get back to you in 48 hours and say, here's my report.\nAnd it will do it better than any human employee, and it will do it,\nbut may be 1/100 the cost.\nWe are going in an age of instant results. you have heard of Software As A service,\nwe are about to enter Results As A Service, RAAS.\nBut that is just the beginning."
subprocess.Popen('notepad.exe')
time.sleep(1)
pyautogui.typewrite(text, interval=0.055)
pyautogui.press('enter')