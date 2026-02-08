import streamlit as st
import statistics

st.set_page_config(page_title="LogicMaster AI", layout="centered")

st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    h1 { color: #00ffcc; text-align: center; }
    .target-box { background-color: #1e1e1e; padding: 20px; border-radius: 15px; border: 2px solid #00ffcc; text-align: center; }
    .target-val { color: #00ffcc; font-size: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def calculate_next_target(history, last_error):
    if len(history) < 6: return None
    last_5 = history[-6:-1]
    pivot = history[-1]
    avg_5 = statistics.mean(last_5)
    low_count = sum(1 for n in history[-6:] if n < 1.40)
    gap_1 = abs(history[-2] - history[-3])
    gap_2 = abs(history[-1] - history[-2])
    is_shrinking = gap_2 < gap_1
    if any(n > 12 for n in history[-6:]) or low_count >= 3:
        target = 1.15 + (pivot * 0.05)
    elif pivot > avg_5:
        target = pivot * 0.82 if is_shrinking else pivot * 1.10
    else:
        target = avg_5 * 0.65 if (pivot % 1) < (history[-2] % 1) else avg_5 * 0.88
    return max(1.01, round(target + (last_error * 0.4), 2))

st.title("🎯 LOGICMASTER AI PRO")
if 'history' not in st.session_state: st.session_state.history = []
if 'last_error' not in st.session_state: st.session_state.last_error = 0
if 'prediction' not in st.session_state: st.session_state.prediction = None

if len(st.session_state.history) < 6:
    st.subheader("शुरुआती 6 अंक डालें")
    cols = st.columns(3)
    in1 = cols[0].number_input("नंबर 1", value=1.0, key="n1")
    in2 = cols[1].number_input("नंबर 2", value=1.0, key="n2")
    in3 = cols[2].number_input("नंबर 3", value=1.0, key="n3")
    in4 = cols[0].number_input("नंबर 4", value=1.0, key="n4")
    in5 = cols[1].number_input("नंबर 5", value=1.0, key="n5")
    in6 = cols[2].number_input("नंबर 6 (Pivot)", value=1.0, key="n6")
    if st.button("शुरू करें"):
        st.session_state.history = [in1, in2, in3, in4, in5, in6]
        st.session_state.prediction = calculate_next_target(st.session_state.history, 0)
        st.rerun()
else:
    st.markdown(f'<div class="target-box"><p style="color:white;">अगला टारगेट</p><div class="target-val">{st.session_state.prediction}x</div></div>', unsafe_allow_html=True)
    actual_res = st.number_input("रिजल्ट क्या आया?", value=1.0, step=0.01)
    if st.button("अगला प्रेडिक्शन"):
        st.session_state.last_error = actual_res - st.session_state.prediction
        st.session_state.history.append(actual_res)
        st.session_state.prediction = calculate_next_target(st.session_state.history, st.session_state.last_error)
        st.rerun()
    if st.button("Reset"):
        st.session_state.history = []; st.rerun()
      
