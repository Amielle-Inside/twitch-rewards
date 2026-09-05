#!/usr/bin/env python3
"""
Full OAuth flow test for twitch-rewards using Playwright with Firefox session cookies.
Tests: login page -> Twitch auth -> callback -> pronouns page
"""
import asyncio
import sys
import os
import json

# Add browserauto skill to path
skill_scripts = "/home/Amielle/.hermes/skills/devops/browserauto/scripts"
sys.path.insert(0, skill_scripts)

from browserauto import load_firefox_session
from playwright.async_api import async_playwright

BASE_URL = "https://newsinsides.ddns.net"


async def test_oauth_flow():
    # Load Firefox cookies
    print("Loading Firefox session cookies...")
    cookies = load_firefox_session()
    
    # Filter cookies for our domains
    twitch_cookies = [c for c in cookies if 'twitch' in c.get('domain', '') or 'id.twitch.tv' in c.get('domain', '')]
    newsinside_cookies = [c for c in cookies if 'newsinsides' in c.get('domain', '')]
    print(f"Found {len(twitch_cookies)} Twitch cookies, {len(newsinside_cookies)} newsinsides cookies")
    
    async with async_playwright() as p:
        # Launch browser in headless mode (no display needed)
        chromium_path = "/home/Amielle/.cache/ms-playwright/chromium-1208/chrome-linux64/chrome"
        browser = await p.chromium.launch(
            executable_path=chromium_path,
            headless=True, 
            args=['--ignore-certificate-errors', '--no-sandbox', '--disable-dev-shm-usage']
        )
        context = await browser.new_context(
            ignore_https_errors=True,
            viewport={'width': 1280, 'height': 720}
        )
        
        # Add Firefox cookies to context
        for cookie in cookies:
            # Playwright cookie format
            pw_cookie = {
                'name': cookie['name'],
                'value': cookie['value'],
                'domain': cookie['domain'],
                'path': cookie['path'],
                'secure': cookie['secure'],
                'httpOnly': cookie['httpOnly'],
            }
            if cookie.get('expiry'):
                pw_cookie['expires'] = cookie['expiry'] // 1000  # Convert ms to seconds
            try:
                await context.add_cookies([pw_cookie])
            except Exception as e:
                pass  # Skip invalid cookies
        
        page = await context.new_page()
        
        # Enable console logging
        page.on("console", lambda msg: print(f"[CONSOLE] {msg.text}"))
        page.on("pageerror", lambda err: print(f"[PAGE ERROR] {err}"))
        
        print(f"\n=== Step 1: Navigate to {BASE_URL}/login ===")
        response = await page.goto(f"{BASE_URL}/login", wait_until="networkidle")
        print(f"Status: {response.status}")
        print(f"URL: {page.url}")
        
        # Check page content
        content = await page.content()
        print(f"Page loaded, length: {len(content)}")
        
        # Find and click "Logar com a Twitch" link
        print("\n=== Step 2: Click Twitch login link ===")
        twitch_link = await page.query_selector('a[href*="id.twitch.tv/oauth2/authorize"]')
        if twitch_link:
            href = await twitch_link.get_attribute('href')
            print(f"Twitch OAuth URL: {href}")
            
            # Navigate to Twitch OAuth
            await page.goto(href, wait_until="domcontentloaded", timeout=60000)
            print(f"Navigated to: {page.url}")
            
            # Check if we're on Twitch login page
            if "id.twitch.tv" in page.url:
                print("On Twitch login page - checking for auto-login via cookies...")
                
                # Wait a bit for cookies to work
                await page.wait_for_timeout(5000)
                
                # Check if we're redirected
                print(f"Current URL: {page.url}")
                
                # If still on Twitch, we may need manual login
                if "id.twitch.tv" in page.url:
                    print("Still on Twitch login - waiting for redirect (2 min timeout)...")
                    try:
                        await page.wait_for_url(f"{BASE_URL}/token**", timeout=120000)
                        print(f"Redirected back to: {page.url}")
                    except Exception as e:
                        print(f"Timeout waiting for redirect: {e}")
                        content = await page.content()
                        print(f"Current page content: {content[:500]}")
                        await browser.close()
                        return False
            
            # Check if we're on /token page
            if "/token" in page.url:
                print("\n=== Step 3: On /token callback page ===")
                # The token.js should auto-POST the code
                await page.wait_for_timeout(3000)  # Wait for JS to execute
                
                # Check for redirect to home
                try:
                    await page.wait_for_url(f"{BASE_URL}/", timeout=10000)
                    print(f"Redirected to home: {page.url}")
                except Exception as e:
                    print(f"Did not redirect to home: {e}")
                    content = await page.content()
                    print(f"Page content: {content[:500]}")
            
            # Check final page
            if page.url == f"{BASE_URL}/" or page.url == f"{BASE_URL}":
                print("\n=== Step 4: On pronouns page ===")
                content = await page.content()
                if "pronouns" in content.lower() or "Escolha seus pronomes" in content:
                    print("SUCCESS: Pronouns page loaded!")
                    print("Page contains pronoun selector")
                    await browser.close()
                    return True
                else:
                    print("Page loaded but no pronouns content found")
                    print(f"Content preview: {content[:500]}")
            else:
                print(f"Final URL: {page.url}")
                content = await page.content()
                print(f"Content preview: {content[:500]}")
        else:
            print("ERROR: Could not find Twitch login link")
            content = await page.content()
            print(f"Page content: {content[:500]}")
        
        await browser.close()
        return False


if __name__ == "__main__":
    result = asyncio.run(test_oauth_flow())
    sys.exit(0 if result else 1)