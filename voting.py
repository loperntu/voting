import streamlit as st
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

def calculate_borda_rankings_alternative(df):
    candidates = df.index.tolist()
    scores = {candidate: 0 for candidate in candidates}
    
    num_candidates = len(candidates)
    for candidate, row in df.iterrows():
        for score in row:
            # Ensure the score is an integer
            try:
                score = int(score)
            except ValueError:
                st.error(f"Invalid score '{score}' for candidate '{candidate}'. Please ensure all scores are integers.")
                return
            scores[candidate] += num_candidates - score
    
    rankings = pd.Series(scores).sort_values(ascending=False)
    return rankings

def plot_results(rankings):
    fm.fontManager.addfont('TaipeiSansTCBeta-Regular.ttf')
    mpl.rc('font', family='Taipei Sans TC Beta')
    # mpl.font_manager.fontManager.addfont('SimHei.ttf') # 臨時註冊新的全局字體
    # plt.rcParams['font.sans-serif']=['SimHei'] #用来正常顯示中文標籤
    # plt.rcParams['axes.unicode_minus']=False #用来正常顯示負號
    # plt.rcParams['font.sans-serif'] = ['Noto Sans CJK TC']  # Specify the font to use    plt.rcParams['axes.unicode_minus'] = False  # Ensure minus signs are displayed correctly

    fig, ax = plt.subplots()
    ax.bar(rankings.index, rankings.values)
    ax.set_ylabel('Borda Score')
    ax.set_xlabel('Candidates')
    ax.set_title('Borda Count Voting Results')
    plt.xticks(rotation=45)
    return fig

st.title('獎學金審議排序計算')
st.header('Ranking base on Borda counting method')

# display markdown
# st.markdown("# 這是一個標題")

st.text('用來方便計算投票排序結果')

uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, index_col='姓名')
    #highlight the min value
    st.dataframe(df.style.highlight_min(axis=0))
    # st.write(df)
    

    rankings = calculate_borda_rankings_alternative(df.iloc[:, 2:])  # exclude non-ranking columns
    
    st.subheader('Rankings')
    st.write(rankings)
    
    st.subheader('Visualization')
    fig = plot_results(rankings)
    st.pyplot(fig)
