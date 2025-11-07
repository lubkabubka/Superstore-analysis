## Ключевые наблюдения

- Общий loss rate — 18.07% *(905 убыточных из 5 009 заказов)*.  
- Среди заказов со скидкой — 34.73% *(905 из 2 606)*: это +16.66 п.п. к общему и риск убыточности в 1.92× выше.  
- 100% убыточных заказов — со скидкой *(905/905)*.  
- Гипотеза: скидочная политика допускает убыточные заказы.  
- Действия:
  1) изменение скидочной политики так, чтобы она не допускала убыточных продаж
  2) ограничение скидок по категориям с высоким discounted loss rate;

<sub>Определение: *Loss rate* — доля заказов, у которых суммарная прибыль по Order ID отрицательна.</sub>

---

## Дашборд (Streamlit)
Функциональность:
- Фильтры: диапазон дат, мультивыбор категорий.
- KPI-плашки: Loss Rate и Loss Rate (со скидкой).

Скриншоты:
![Dashboard KPIs1](media/dashboard_kpi.png)
![Dashboard KPIs2](media/dashboard_kpi_also.png)

---

## Запуск
# 1) создать окружение
python -m venv venv
# Linux/macOS
source venv/bin/activate
# Windows (PowerShell)
# .\venv\Scripts\Activate.ps1

# 2) поставить зависимости
pip install -r requirements.txt

# 3) структура данных
# положи SQLite в data/db.sqlite (или укажи свой путь в app/streamlit_app.py)

# 4) запустить дашборд
streamlit run app/streamlit_app.py

--- 
## Requirements
pandas
sqlalchemy
streamlit
---