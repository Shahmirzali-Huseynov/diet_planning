import pandas as pd
import pulp as pl
from collections import defaultdict
import random
from models import Meal, NutrientValues, DayMenu, WeeklyMenu


def get_diet_menu():
    df1 = pd.read_csv("assets/set1.csv")
    df2 = pd.read_csv("assets/set2.csv")

    df1_indexed = df1.set_index("ID")

    age = 20
    gender = "Kadın"

    def find_mandatory_dish_id(df, used_dishes):
        for dish_name in mandatory_dish_names:
            dish_row = df[df["Yiyecek adı"] == dish_name]
            if not dish_row.empty:
                dish_id = dish_row.iloc[0]["ID"]
                if dish_id not in used_dishes:
                    return dish_id, dish_name
        return None, None

    limits = df2[
        (df2["Cinsiyet"] == gender)
        & (df2["Yaş Grubu"].apply(lambda x: age in range(*map(int, x.split("-")))))
    ].iloc[0]

    all_mandatory_dish_names = [
        "Etli Nohut",
        "Etli Kuru Fasulye",
        "Zeytinyağlı Barbunya",
        "Börülce Salatası",
        "Mercimek Salatası",
        "Piyaz",
    ]

    mandatory_dish_names = random.sample(all_mandatory_dish_names, 4)

    mandatory_dish_ids = [
        df1[df1["Yiyecek adı"] == name].iloc[0]["ID"]
        for name in mandatory_dish_names
        if not df1[df1["Yiyecek adı"] == name].empty
    ]

    # print(f"Zorunlu yemekler: {mandatory_dish_names} ve idleri: {mandatory_dish_ids}")

    categories = {
        "main": range(1, 72),
        "soup": range(72, 100),
        "half_main": range(100, 150),
        "dessert_salad": range(150, 210),
    }

    vegetable_meals_ids = [
        123,
        124,
        125,
        126,
        127,
        128,
        130,
        131,
        132,
        133,
        144,
        145,
        146,
        147,
        148,
        149,
        150,
    ]
    salad_meals_ids = df1[
        df1["Yiyecek adı"].str.contains("Salata")
        & df1["ID"].isin(categories["dessert_salad"])
    ]["ID"].tolist()

    soup_meals_ids = [
        71,
        72,
        73,
        74,
        75,
        76,
        77,
        78,
        79,
        80,
        81,
        82,
        83,
        84,
        85,
        86,
        87,
        88,
        89,
        90,
        91,
        92,
        93,
        94,
        95,
        96,
        97,
        98,
        99,
        100,
    ]
    compote_hosaf_meals_ids = [167, 168, 169, 170, 171]

    etli_dolma_sarma_ids = df1[
        df1["Yiyecek adı"].str.contains("Etli")
        & (
            df1["Yiyecek adı"].str.contains("Dolma")
            | df1["Yiyecek adı"].str.contains("Sarma")
        )
    ]["ID"].tolist()

    pilav_ids = df1[df1["Yiyecek adı"].str.contains("Pilav")]["ID"].tolist()

    # Pirinç pilavı, yayla çorbası ve sütlaç aynı güne verilmemelidir.
    specified_meal_ids = df1[
        df1["Yiyecek adı"].str.contains(
            "Pirinç Pilavı|Şehriyeli Pirinç Pilavı|Yayla Çorbası|Sütlaç", regex=True
        )
    ]["ID"].tolist()

    price_conversion = {"a": 5, "b": 4, "c": 3, "d": 2, "e": 1}

    used_dishes = set()
    used_mandatory_dishes = set()

    df1["Renk"] = df1["Renk"].str.lower()
    df1["Kıvam"] = df1["Kıvam"].str.lower()

    available_colors = df1["Renk"].drop_duplicates().values.tolist()
    available_textures = df1["Kıvam"].drop_duplicates().values.tolist()

    weekly_menus = []

    for week in range(1, 5):
        # print(f"{week}. Hafta Menüleri\n")
        mandatory_dish_day = random.choice(range(1, 6))
        mandatory_dish_id, mandatory_dish_name = None, None

        weekly_menu = WeeklyMenu(Hafta=week, Menuler=[]) 

        for day in range(1, 6):
            prob = pl.LpProblem(f"Menu_Optimization_{week}_{day}", pl.LpMinimize)

            available_dishes = list(
                set(df1["ID"]) - used_dishes - set(mandatory_dish_ids)
            )

            if day == mandatory_dish_day:
                # available_dishes = list(set(df1["ID"]) - used_dishes)
                available_dishes = list(
                    set(df1["ID"]) - used_dishes - set(mandatory_dish_ids[week:])
                )

            dish_vars = pl.LpVariable.dicts("Dish", available_dishes, 0, 1, pl.LpBinary)

            prob += pl.lpSum(
                [
                    price_conversion[df1_indexed.loc[i]["Fiyat"]] * dish_vars[i]
                    for i in available_dishes
                ]
            )

            for nutrient in ["Enerji", "Karbonhidrat", "Protein", "Yağ", "Lif"]:
                lower_limit = float(limits[nutrient].split("-")[0])
                upper_limit = float(limits[nutrient].split("-")[1])

                prob += pl.LpConstraint(
                    e=pl.lpSum(
                        [
                            df1_indexed.loc[i][nutrient] * dish_vars[i]
                            for i in available_dishes
                        ]
                    ),
                    sense=pl.LpConstraintGE,
                    name=f"{nutrient}_lower_bound",
                    rhs=lower_limit,
                )

                prob += pl.LpConstraint(
                    e=pl.lpSum(
                        [
                            df1_indexed.loc[i][nutrient] * dish_vars[i]
                            for i in available_dishes
                        ]
                    ),
                    sense=pl.LpConstraintLE,
                    name=f"{nutrient}_upper_bound",
                    rhs=upper_limit,
                )

            for cat, rng in categories.items():
                prob += (
                    pl.lpSum([dish_vars[i] for i in available_dishes if i in rng]) == 1
                )

            for color in available_colors:
                prob += (
                    pl.lpSum(
                        [
                            dish_vars[i]
                            for i in available_dishes
                            if df1_indexed.loc[i]["Renk"] == color
                        ]
                    )
                    <= 2
                )
            for texture in available_textures:
                prob += (
                    pl.lpSum(
                        [
                            dish_vars[i]
                            for i in available_dishes
                            if df1_indexed.loc[i]["Kıvam"] == texture
                        ]
                    )
                    <= 2
                )

            for veg_meal_id in vegetable_meals_ids:
                for salad_meal_id in salad_meals_ids:
                    if (
                        veg_meal_id in available_dishes
                        and salad_meal_id in available_dishes
                    ):
                        prob += dish_vars[veg_meal_id] + dish_vars[salad_meal_id] <= 1

            for soup_meal_id in soup_meals_ids:
                for compote_hosaf_meal_id in compote_hosaf_meals_ids:
                    if (
                        soup_meal_id in available_dishes
                        and compote_hosaf_meal_id in available_dishes
                    ):
                        prob += (
                            dish_vars[soup_meal_id] + dish_vars[compote_hosaf_meal_id]
                            <= 1
                        )

            for etli_dolma_sarma_id in etli_dolma_sarma_ids:
                for pilav_id in pilav_ids:
                    if (
                        etli_dolma_sarma_id in available_dishes
                        and pilav_id in available_dishes
                    ):
                        prob += (
                            dish_vars[etli_dolma_sarma_id] + dish_vars[pilav_id] <= 1
                        )
            specified_meal_ids = [
                meal_id for meal_id in specified_meal_ids if meal_id in dish_vars
            ]
            prob += (
                pl.lpSum([dish_vars[meal_id] for meal_id in specified_meal_ids]) <= 1
            )

            if day == mandatory_dish_day:
                mandatory_dish_id, mandatory_dish_name = find_mandatory_dish_id(
                    df1, used_mandatory_dishes
                )
                if mandatory_dish_id is None:
                    print("Uygun zorunlu yemek kalmadı.")
                else:
                    used_mandatory_dishes.add(mandatory_dish_id)
                    prob += dish_vars[mandatory_dish_id] == 1
                    used_dishes.add(mandatory_dish_id)

            prob.solve(pl.PULP_CBC_CMD(msg=False))
            # print(f"{day}. Gün Menüsü:")
            total_nutrients = defaultdict(float)

            for v in prob.variables():
                if v.varValue == 1:
                    dish_id = int(v.name.split("_")[1])
                    # dish_info = df1_indexed.loc[dish_id]
                    # print(
                    #     f"ID: {dish_id}, Yemek: {dish_info['Yiyecek adı']}, Fiyat: {dish_info['Fiyat']}, Renk: {dish_info['Renk']}, Kıvam: {dish_info['Kıvam']}"
                    # )
                    # for nutrient in ["Enerji", "Karbonhidrat", "Protein", "Yağ", "Lif"]:
                    #     total_nutrients[nutrient] += dish_info[nutrient]

                    used_dishes.add(dish_id)

            # print("Toplam Besin Değerleri:")
            # for nutrient, value in total_nutrients.items():
            #     print(f"{nutrient}: {value}")
            selected_dishes = [i for i in available_dishes if dish_vars[i].value() == 1]
            day_menu_meals = [Meal(
                ID=int(i),
                Yemek=df1_indexed.loc[i]["Yiyecek adı"],
                Fiyat=df1_indexed.loc[i]["Fiyat"],
                Renk=df1_indexed.loc[i]["Renk"],
                Kivam=df1_indexed.loc[i]["Kıvam"]
            ) for i in selected_dishes]
            
            total_nutrient_values = NutrientValues(
                Enerji=sum(df1_indexed.loc[i]["Enerji"] for i in selected_dishes),
                Karbonhidrat=sum(df1_indexed.loc[i]["Karbonhidrat"] for i in selected_dishes),
                Protein=sum(df1_indexed.loc[i]["Protein"] for i in selected_dishes),
                Yağ=sum(df1_indexed.loc[i]["Yağ"] for i in selected_dishes),
                Lif=sum(df1_indexed.loc[i]["Lif"] for i in selected_dishes)
            )
            
            day_menu = DayMenu(Status="Optimal", Day= day, Gun_Menu=day_menu_meals, Toplam_Besin_Degerleri=total_nutrient_values)
            weekly_menu.Menuler.append(day_menu)

        weekly_menus.append(weekly_menu)

    return weekly_menus
