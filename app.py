import streamlit as st



from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.service import Service
import time
from bs4 import BeautifulSoup

# ------------- Settings for Pages -----------
st.set_page_config(layout="wide")

# Keep text only
@st.cache_data(ttl=3600)
def get_website_content(url):
    driver = None
    try:
        # Using on Local
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1200')
        driver = webdriver.Chrome(service=Service(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()),
                                  options=options)
        print(f"DEBUG:DRIVER:{driver}")
        driver.get(url)
        time.sleep(10)
        html_doc = driver.page_source
        driver.quit()
        soup = BeautifulSoup(html_doc, "html.parser")
        return soup.get_text()
    except Exception as e:
        print(f"DEBUG:INIT_DRIVER:ERROR:{e}")
    finally:
        if driver is not None: driver.quit()
    return None


def show_summary(article_json):
    summary_html = f"""<div style="padding: 10px; border-radius: 5px;">
                                        <p> Nội dung tóm tắt của bài viết: </p>
                                        <h4 style="color: darkgreen;">{article_json["title"]}</h4>
                                        <p> Ngày xuất bản:{article_json["publish_date"]}</p>
                                        <p> {article_json["summary"]}</p>
                                        </div>"""
    st.markdown(summary_html, unsafe_allow_html=True)


# ---------------- Page & UI/UX Components ------------------------
def main_sidebar():
    # 1.Vertical Menu
    st.header("Running Selenium on Streamlit Cloud")
    site_extraction_page()


def site_extraction_page():
    SAMPLE_URL = "https://www.vib.com.vn/vn/the-tin-dung/vib-financial-free"
    url = st.text_input(label="URL", placeholder="https://example.com", value=SAMPLE_URL)

    clicked = st.button("Load Page Content",type="primary")
    if clicked:
        with st.container(border=True):
            with st.spinner("Đang tải nội dung website..."):
                content = get_website_content(url)
                st.write(content)


if __name__ == "__main__":
    main_sidebar()
