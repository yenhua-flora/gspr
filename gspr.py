import pandas as pd
import streamlit as st
import plotly.express as px
import datetime
import seaborn as sns
import matplotlib.pyplot as plt
import openpyxl
import pip
import numpy as np

import sqlite3

# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_squared_error, r2_score
# import base64
# import io





#---------------------------------#
# Hide menu in Streamlit apps
hide = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """
st.markdown(hide, unsafe_allow_html=True)



#---------------------------------#
# Create the Home page
def Home():
    st.title("Medical Device Regulation Decision Tool :stethoscope: ")

    st.markdown("""
                
                Research Title: Design of a Medical Device Regulation Decision Tool

                Thank you so much for taking the time to participate in this research for a postgraduate student dissertation. This study aims to design a decision tool to correctly filter and select the appropriate regulatory requirements that need to be met by medical devices. After testing this tool, collect user experience to efficiently analyse search results and improve the system application for encouraging widespread use in the future.

                In more detail, this system briefly analyses the European Union (EU) regulation requirements with relative standards for medical devices from the European Medical Device Nomenclature (EMDN), which according to Annex I: general safety and performance requirements (GSPR) as listed in the Medical Device Regulation (MDR) (2017/745) as well as the In Vitro Diagnostic Medical Devices Regulation (IVDR) (2017/746).
                * **MDR:** [Regulation (EU) 2017/745 of the European Parliament and of the Council of 5 April 2017 on medical devices](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32017R0745)
                * **IVDR:** [Regulation (EU) 2017/746 of the European Parliament and of the Council of 5 April 2017 on in vitro diagnostic medical devices](https://eur-lex.europa.eu/eli/reg/2017/746/oj)
                * **EMDN:** [European Medical Device Nomenclature (EMDN)](https://webgate.ec.europa.eu/dyna2/emdn/)

                User participation in this research study is entirely voluntary and will take around 5 minutes to complete. The survey is anonymous, and the users' answers will only be utilized for the purpose of writing a research report. Any report or publication resulting from this study cannot and will not personally identify the user.
                
                Please be aware that all information this system provides is for reference only, as regulations are updated frequently and the database may delay follow-up. If you have any questions or require more information about this research, please use the following contact email: k23018577@kcl.ac.uk
                """)
    
    st.markdown("""
                            
                研究主題：醫療器材監管決策工具的設計

                非常感謝您抽出寶貴時間參與這項碩士生論文研究。本研究旨在設計一種決策工具，以正確過濾和選擇醫療器材所需滿足的適當監管要求。經過測試後收集使用者體驗，以有效分析搜尋結果並改善應用系統進一步促進未來廣泛的使用。

                該系統根據歐洲醫療器材命名法(EMDN)所提及的醫療器材，簡要分析了歐盟(EU)法規要求的相關標準。而歐盟法規來源於參考醫療器材法規(MDR)(2017/745)、以及體外診斷醫療器材法規(IVDR)(2017/746)中，其中附件一的一般安全和性能要求(GSPR)所列出內容。
                * **醫療器材法規:** [Regulation (EU) 2017/745 of the European Parliament and of the Council of 5 April 2017 on medical devices](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX%3A32017R0745)
                * **體外診斷醫療器材法規:** [Regulation (EU) 2017/746 of the European Parliament and of the Council of 5 April 2017 on in vitro diagnostic medical devices](https://eur-lex.europa.eu/eli/reg/2017/746/oj)
                * **歐洲醫療器材命名法:** [European Medical Device Nomenclature (EMDN)](https://webgate.ec.europa.eu/dyna2/emdn/)

                使用者參與本研究完全是自願的，花費時間約3~5分鐘完成。該調查是匿名的，使用戶的回答將僅用於撰寫研究報告為目的。而本研究產生的任何報告或出版物不能也不會識別使用者的個人身分。
                
                請注意，本系統提供的所有資訊僅供參考，因法規日益更新而資料庫可能延遲跟進。如果您對於本研究有任何疑問或需要更多信息，請透過以下電子郵件聯絡：k23018577@kcl.ac.uk
                """)



#---------------------------------#
# Load excel data
excel_E = pd.ExcelFile('GSPRen.xlsx') # Load the excel data in English
emdn_E = pd.read_excel(excel_E, sheet_name='EMDN', na_filter=False, header=2) # Load excel worksheet of EMDN
excel_C = pd.ExcelFile('GSPRcn.xlsx') # Load the excel data in Mandarin
emdn_C = pd.read_excel(excel_C, sheet_name='EMDN', na_filter=False, header=2) # Load excel worksheet of EMDN


def EMDN(): # Create the EMDN page
    st.header(" :star2:  General Safety and Performance Requirements 一般安全和性能要求")
    st.markdown("""
                Thank you so much for testing the system function. The table below shows each EMDN code category and type corresponds with specific medical device data. Please select English or Mandarin to offer the EMDN code you would like to search for; then, the system will load the related information immediately. 
                
                非常感謝您測試本系統的功能。下表顯示了每個 EMDN 代碼類別和類型對應特定的醫療器材資料。請選擇英文或中文給予預計搜尋之 EMDN 代碼；然後，系統會立即載入相關資訊供您參考。
                """)
    
    col1, col2 = st.tabs(["EMDN code","EMDN 代碼"])

    with col1:  # Create the EMDN page in English
        st.header("EMDN code")
        st.write("""Shown is the European Medical Device Nomenclature (EMDN) structure, which characterizes medical device information into different levels""")
        st.dataframe(emdn_E) # Display the EMDN code data

        category_E = st.selectbox("Please select the EMDN code category", list(emdn_E)) # List the EMDN code category
        group_E = emdn_E.groupby(by=[category_E], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
        type_E = st.selectbox("Please select the EMDN code type", list(group_E.iloc[:,0])) # List each EMDN code type so the user can select which medical device to search for 

        if st.button("Search"): # Set up the button
            st.success("Please wait a few minutes; the page turns on medical device: {} information".format(type_E))
            GSPR_E(type_E) # The EMDN type will retun to the GSPR_E function


    with col2:  # Create the EMDN page in Mandarin
        st.header("EMDN 代碼")
        st.write("""表格所示為歐洲醫療器材命名法(EMDN)結構，該結構將醫療器材劃分為不同種類""")
        st.dataframe(emdn_C) # Display the EMDN code data in Mandarin

        category_C = st.selectbox("請選擇 EMDN 代碼類別", list(emdn_C)) # List the EMDN code category
        group_C = emdn_C.groupby(by=[category_C], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
        type_C = st.selectbox("請選擇 EMDN 代碼類型", list(group_C.iloc[:,0])) # List each EMDN code type so the user can select which medical device to search for 

        if st.button("搜尋"): # Set up the button
            st.success("請稍等幾分鐘；頁面將開啟: {}的醫療器材資訊".format(type_C))
            GSPR_C(type_C)



def GSPR_E(type_E):  # Create the GSPR page in English
    st.write("The {} information shown can be searched, fullscreen, and downloaded as an Excel file for personal records and edits".format(type_E))
    
    
    # Set up different tabs
    ChapterI, ChapterII, ChapterIII, Standards = st.tabs(["Chapter I", "Chapter II", "Chapter III", "Standards"])

    with ChapterI: # Get Chapter I General requirements details in English
        st.subheader("{}".format(pd.read_excel(excel_E, sheet_name=type_E, usecols="A", header=1).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterI_E = pd.read_excel(excel_E, sheet_name=type_E, na_filter=False, usecols="A:D", header=2) # replace NaN as blank, read the columns from A to C to get English details, and the header is 2nd row of excel
        chapterI_E = chapterI_E.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        chapterI_E = chapterI_E.iloc[:22] # Selecting all row from header 2 to row 22
        st.dataframe(chapterI_E)

        # apply_chapterI_E = chapterI_E['Apply Y/N'].unique()
        # apply_chapterI_E = st.multiselect("Select apply:", options=option_chapterI_E)
        # standard_chapterI_E = chapterI_E['Relevant Standard(s)'].unique()
        # standard_chapterI_E = st.multiselect("Select standard:", options=standard_chapterI_E)
        # filter_chapterI_E = chapterI_E[chapterI_E['Apply Y/N'].isin(select_chapterI_E)]    
        # st.dataframe(filter_chapterI_E)
    

    with ChapterII: # Get Chapter II Requirements regarding design and manufacture details in English
        st.subheader("{}".format(pd.read_excel(excel_E, sheet_name=type_E, usecols="A", header=25).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterII_E = pd.read_excel(excel_E, sheet_name=type_E, na_filter=False, usecols="A:D", header=26)
        chapterII_E = chapterII_E.replace("\n", ", ", regex=True) 
        chapterII_E = chapterII_E.iloc[:141] # Selecting all row from header 26 to row 141
        st.dataframe(chapterII_E)

    with ChapterIII: # Get Chapter III Requirements regarding the information supplied with the device details in English
        st.subheader("{}".format(pd.read_excel(excel_E, sheet_name=type_E, usecols="A", header=168).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterIII_E = pd.read_excel(excel_E, sheet_name=type_E, na_filter=False, usecols="A:D", header=169)
        chapterIII_E = chapterIII_E.replace("\n", ", ", regex=True) 
        chapterIII_E = chapterIII_E.iloc[:265]
        st.dataframe(chapterIII_E)

    with Standards: # Get Standard details in English
        st.subheader("Standards List")
        standards_E = pd.read_excel(excel_E, sheet_name=type_E, na_filter = False, usecols="F:G", header=2) # replace NaN as blank
        standards_E = standards_E.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        standards_E = standards_E.iloc[:30]
        st.dataframe(standards_E)



def GSPR_C(type_C):  # Create the GSPR page in Mandarin
    st.write("顯示的資訊結果可以搜尋、全螢幕顯示，也可以下載為Excel檔案，以供個人記錄和編輯")

    #Set up different tabs
    第一章, 第二章, 第三章, 標準清單 = st.tabs(["第一章", "第二章", "第三章", "標準清單"])

    with 第一章: # Get Chapter I General requirements details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel_C, sheet_name=type_C, usecols="A", header=1).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterI_C = pd.read_excel(excel_C, sheet_name=type_C, na_filter=False, usecols="A:D", header=2)  # replace NaN as blank, read the columns from E to G to get Chinese details, and the header is 2nd row of excel
        chapterI_C = chapterI_C.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        chapterI_C = chapterI_C.iloc[:22] # Selecting all row from header 2 to row 22
        st.dataframe(chapterI_C)

    with 第二章: # Get Chapter II Requirements regarding design and manufacture details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel_C, sheet_name=type_C, usecols="A", header=25).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterII_C = pd.read_excel(excel_C, sheet_name=type_C, na_filter=False, usecols="A:D", header=26)
        chapterII_C = chapterII_C.replace("\n", ", ", regex=True) 
        chapterII_C = chapterII_C.iloc[:141]
        st.dataframe(chapterII_C)

    with 第三章: # Get Chapter III Requirements regarding the information supplied with the device details in Mandarin
        st.subheader("{}".format(pd.read_excel(excel_C, sheet_name=type_C, usecols="A", header=168).iloc[0,0])) # use iloc to read the value of one cell as a header
        chapterIII_C = pd.read_excel(excel_C, sheet_name=type_C, na_filter=False, usecols="A:D", header=169)
        chapterIII_C = chapterIII_C.replace("\n", ", ", regex=True) 
        chapterIII_C = chapterIII_C.iloc[:265]
        st.dataframe(chapterIII_C)

    with 標準清單: # Get Standard details in Mandarin
        st.subheader("標準清單")
        standards_C = pd.read_excel(excel_C, sheet_name=type_C, na_filter = False, usecols="F:G", header=2) # replace NaN as blank
        standards_C = standards_C.replace("\n", ", ", regex=True) # without wrap text function by replacing \n as comma 
        standards_C = standards_C.iloc[:30]
        st.dataframe(standards_C)




#---------------------------------#
def Survey(): # Collecting user inputs for later analysis
    st.header(" :memo: Survey 調查")
    st.markdown("""
                Thank you so much for providing your experience after testing this system in English or Mandarin for later analysis, and the collected result data will displayed on the next page for every participant to understand more information. :thought_balloon:
                
                非常感謝您在測試系統後，提供英文或中文的使用經驗供後續分析，而收集的結果數據將顯示在下一頁，供每位參與者了解更多信息。:thought_balloon:
                """)
    col1, col2 = st.tabs(["User Experience Survey", "使用者體驗調查"])

    #conn = sqlite3.connect('Survey.db', check_same_thread=False) # Establishing a SQL data
    #cursor = conn.cursor()
    

    
    with col1:
        st.subheader("User Experience Survey")
        date = st.text_input("Date ", (datetime.date.today()), disabled=True)
        background = st.selectbox("Please select the business type of your background?", ("", "Academics", "Manufacturer", "Importer", "Distributor", "Wholesaler","Retailer", "Others",))
        role = st.selectbox("Please select your current role?", ("", "Professionals", "Professor", "Student", "Manager", "Engineer", "Officer", "Sales Representative", "Assistant", "Others", "Prefer not to say"))

        EMDN_category = st.selectbox("Which EMDN category of medical device are you particularly interested in searching for?", list(emdn_E)) # set index to none means there is no default options
        group_E = emdn_E.groupby(by=[EMDN_category], as_index=False)[[]].sum() # Group the EMDN code type based on the specific category chosen
        EMDN_type = st.selectbox("Which EMDN type of medical device are you particularly interested in searching for?", list(group_E.iloc[:,0]))
        
        information = st.selectbox("How would you rate the provided device information on this website overall?", ("","1: Absolutely appropriate and clear", "2: Appropriate and clear", "3: Neutral", "4: Inappropriate and unclear", "5: Absolutely inappropriate and unclear"))
        experience = st.selectbox("How would you rate your overall experience with this website on a scale?", ("","1: Extremely useful", "2: Slightly useful", "3: Neither useful nor useless", "4: Slightly useless", "5: Extremely useless"))
        others = st.text_area("What other information would you like to see on this page? (Optional)")
        feedback = st.text_area("Do you have any additional comments, concerns, feedback, or suggestions on this system that we could improve? (Optional)")
        submit = st.button(label="Submit")
        
        if submit == True: # if the submit button is pressed
            #st.success("Successfully submitted. !! Thank you so much for your support !! ") 
            info_E(date, background, role, EMDN_category, EMDN_type, information, experience, others, feedback)



            
            # userdata_E = pd.DataFrame([{
            #     "Date": day,
            #     "Background": background,
            #     "Role": role,
            #     "EMDN Category": device_category,
            #     "EMDN Type": device_type,
            #     "Device Information": clear,
            #     "Overall Experience": useful,
            #     "What other information would you like to see on this page?": information,
            #     "Do you have any additional comments, concerns, feedback, or suggestions on this system that we could improve?": feedback
            #     }])
            # update_E = pd.concat([survey_data, userdata_E], ignore_idex=True) # add the user input data to the survey excel
            # conn.update(worksheet="Survey", data=update_E) # update google sheets with the user input data
            # st.success("Successfully submitted. !! Thank you so much for your support !! ")    


        # if st.button(label="Submit"): # if the submit button is pressed
        #     userdata = pd.concat([pd.read_excel("Survey.xlsx"), pd.DataFrame.from_records([{
        #         "Date": day,
        #         "Background": background,
        #         "Role": role,
        #         "EMDN Category": device_category,
        #         "EMDN Type": device_type,
        #         "Device Information": clear,
        #         "Overall Experience": useful,
        #         "What other information would you like to see on this page?": information,
        #         "Do you have any additional comments, concerns, feedback, or suggestions on this system that we could improve?": feedback
        #         }])])
        #     userdata.to_excel("Survey.xlsx", index=False)
        #     created_files.append("Survey.xlsx")
            
            
            # st.success("Successfully submitted. !! Thank you so much for your support !! ")


    with col2:
        st.subheader("使用者體驗調查")
        date_C = st.text_input("日期", (datetime.date.today()), disabled=True)
        background_C = st.selectbox("請問您的背景", ("", "學術", "製造商", "進口商", "經銷商", "批發商", "其他",))
        role_C = st.selectbox("請問您目前的職位", ("", "專業人士", "教授", "學生", "經理", "工程師", "專員", "業務", "助理", "其他", "不方便提供"))               
    
        EMDN_category_C = st.selectbox("請問您對哪種 EMDN 分類的醫療器材特別感興趣搜尋?", list(emdn_C)) # set index to none means there is no default options
        group_C = emdn_C.groupby(by=[EMDN_category_C], as_index=False).sum() # Group the EMDN code type based on the specific category chosen
        EMDN_type_C = st.selectbox("請問您對哪種 EMDN 類型的醫療器材特別感興趣搜尋?", list(group_C.iloc[:,0]))

        information_C = st.selectbox("請問您對本網站所提供的整體醫材資訊評價如何？", ("","1: 非常適當和明確", "2: 適當和明確", "3: 普通", "4: 不適當和不明確", "5: 非常不適當和不明確"))
        experience_C = st.selectbox("請問您對本網站的整體體驗有何評價？", ("","1: 非常有用", "2: 稍微有用", "3: 普通", "4: 稍微沒用", "5: 非常沒用"))
        others_C = st.text_area("請問您希望在此頁面上看到哪些其他資訊？")
        feedback_C = st.text_area("請問您對於此系統有任何意見、疑慮、回饋或建議可以幫助我們改進嗎？")
        submit_C = st.button(label="提交")
        
        if submit_C == True: # if the submit button is pressed
            #st.success("提交成功 !! 非常感謝您寶貴的意見及支持 !! ")
            info_C(date_C, background_C, role_C, EMDN_category_C, EMDN_type_C, information_C, experience_C, others_C, feedback_C)


def info_E(a, b, c, d, e, f, g, h, i):
    conn = sqlite3.connect('Survey.db', check_same_thread=False) # Establishing a SQL data
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS survey(Date DATE, Background TEXT, Role TEXT, EMDN_category TEXT, EMDN_type TEXT, Information TEXT, Experience TEXT, Others TEXT, Feedback TEXT)""")
    cursor.execute("INSERT INTO survey VALUES(?,?,?,?,?,?,?,?,?)", (a,b,c,d,e,f,g,h,i))
    conn.commit()
    conn.close()
    st.success("Successfully submitted. !! Thank you so much for your support !! ")


def info_C(a, b, c, d, e, f, g, h, i):
    conn = sqlite3.connect('Survey.db', check_same_thread=False) # Establishing a SQL data
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS survey(日期 DATE, 背景 TEXT, 職位 TEXT, EMDN類別 TEXT, EMDN類型 TEXT, 資材資訊 TEXT, 體驗 TEXT, 其他資訊 TEXT, 回饋 TEXT)""")
    cursor.execute("INSERT INTO survey VALUES(?,?,?,?,?,?,?,?,?)", (a,b,c,d,e,f,g,h,i))
    conn.commit()
    conn.close()
    st.success("提交成功 !! 非常感謝您寶貴的意見及支持 !! ")

    
            
            # userdata_C = pd.DataFrame([{
            #     "日期": day_C,
            #     "背景": background_C,
            #     "職位": role_C,
            #     "EMDN類別": device_category_C,
            #     "EMDN類型": device_type_C,
            #     "醫材資訊": value_C,
            #     "整體體驗": useful_C,
            #     "請問您希望在此頁面上看到哪其他資訊？": information_C,
            #     "請問您對於此系統有任何意見、疑慮、回饋或建議可以幫助我們改進嗎？": feedback_C
            #     }])
            # update_C = pd.concat([survey_data, userdata_C], ignore_idex=True) # add the user input data to the survey excel
            # conn.update(worksheet="Survey", data=update_C) # update google sheets with the user input data
            # st.success("提交成功 !! 非常感謝您寶貴的意見及支持 !! ")
            

        
        # if st.button(label="提交"): # if the submit button is pressed
        #     userdata_C = pd.concat([pd.read_excel("Survey.xlsx"), pd.DataFrame.from_records([{
        #         "日期": day_C,
        #         "背景": background_C,
        #         "職位": role_C,
        #         "EMDN類別": device_category_C,
        #         "EMDN類型": device_type_C,
        #         "醫材資訊": value_C,
        #         "整體體驗": useful_C,
        #         "請問您希望在此頁面上看到哪些其他資訊？": information_C,
        #         "請問您對於此系統有任何意見、疑慮、回饋或建議可以幫助我們改進嗎？": feedback_C
        #         }])])
        #     userdata_C.to_excel("Survey.xlsx", index=False)
            #st.success("提交成功 !! 非常感謝您寶貴的意見及支持 !! ")


        

#---------------------------------#
def Analysis(): # Plotting and data visualisation to analyse user experience survey result
    st.header(" :bar_chart: Data Analysis 數據分析")
    st.markdown("""
                Thank you so much for participating in this research. The data plotting and visualisation shown are according to user experience survey results, which combine information from English and Mandarin for statistical analysis. Please note that the data illustrated is only for personal review because some related information may be incorrect. :blush:
                
                非常感謝您參與這項研究。所顯示的數據圖表和視覺化是根據使用者體驗調查結果，其結合英文和中文的資料進行統計分析。請注意，所示數據僅供個人參考，因為某些相關資訊可能不正確。:blush:
                """)
    
    excel = pd.read_excel('Survey.xlsx')

    Counts, Analysis, 數量, 分析 = st.tabs(["Counts", "Analysis", "數量", "分析"])

    with Counts: # User select the x-axis to plot the counts
        xvalue_E = st.selectbox("Please select X-Axis value to calculate the total values", options=excel.columns[1:7])
        count_E = excel[xvalue_E].value_counts()
        st.bar_chart(count_E)
        expander_E = st.expander("Count Results")
        expander_E.write(count_E)

    with Analysis: # User select the x-axis and y-axis value to plot the analysis data
        xaxis_E = st.selectbox("Please select X-Axis value", options=excel.columns[0:7])
        yaxis_E = st.selectbox("Please select Y-Axis value", options=excel.columns[1:7])
        plot_E = px.scatter(excel, x=xaxis_E, y=yaxis_E, labels={xaxis_E:yaxis_E}, title="The searched {} by {} results".format(xaxis_E,yaxis_E))
        color_E = st.color_picker("Please select the plot color") # user select the particular color                
        plot_E.update_traces(marker=dict(color=color_E)) # Update the plot color after the user chosen
        st.plotly_chart(plot_E, use_container_width=True) # Display the data
        
        expander2_E = st.expander("Analysis Results")
        data2_E = excel[[xaxis_E, yaxis_E]].groupby(by=xaxis_E)[yaxis_E].sum()
        expander2_E.write(data2_E)

    with 數量: # User select the x-axis to plot the counts  
        xvalue_C = st.selectbox("請選擇X軸值來計算總數量", options=excel.columns[11:17])
        count_C = excel[xvalue_C].value_counts()
        st.bar_chart(count_C)
        expander_C = st.expander("計算結果")
        expander_C.write(count_C)

    with 分析: # User select the x-axis and y-axis value to plot the analysis data
        xaxis_C = st.selectbox("請選擇X軸值", options=excel.columns[10:17])
        yaxis_C = st.selectbox("請選擇Y軸值", options=excel.columns[11:17])        
        plot_C = px.scatter(excel, x=xaxis_C, y=yaxis_C, labels={xaxis_C:yaxis_C}, title="依照 {} 搜尋 {} 的結果".format(xaxis_C,yaxis_C))
        st.plotly_chart(plot_C, use_container_width=True) # Display the data
        expander2_C = st.expander("分析結果")
        data2 = excel[[xaxis_C, yaxis_C]].groupby(by=xaxis_C)[yaxis_C].sum()
        expander2_C.write(data2)



#---------------------------------#
# Create the sidebar for choosing the specific page
options = st.sidebar.radio("Pages", options=[":stethoscope: Home", " :star2: GSPR", " :memo: Survey", " :bar_chart: Analysis"])

if options == ":stethoscope: Home":
    Home()
elif options == " :star2: GSPR":
    EMDN()
elif options == " :memo: Survey":
    Survey()
elif options == " :bar_chart: Analysis":
    Analysis()





