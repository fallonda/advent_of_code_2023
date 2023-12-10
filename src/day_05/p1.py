from src.utils import read_text
import numpy as np
from io import StringIO
import pandas as pd

p1_example = read_text("./src/day_05/p1_example.txt")
p1_example.extend("\n")

seeds = []
maps = {}
for i, line in enumerate(p1_example):
    # Get the seed numbers as array
    if i == 0:
        seeds.append(
                np.loadtxt(
                    fname = StringIO(line.split(": ")[1]),
                    dtype = int
                )                
        )
    if "map:" in line:
        title = line.split(" ")[0]
        mapping_list = []
        j = 1
        while p1_example[i+j][0] != "\n":
            mapping_list.append(
                np.loadtxt(
                    fname = StringIO(p1_example[i+j]),
                    dtype = int
                )
            )
            j += 1
        maps[title] = mapping_list  
        
# print(seeds)
# print(maps)

df_dict = {}
for key, value in maps.items():
    first_colname = key.split("-to-")[0]
    second_colname = key.split("-to-")[1]
    source_list = []
    dest_list = []
    for i in value:
        source_list.extend([x for x in range(i[1], i[1]+i[2])])
        dest_list.extend([x for x in range(i[0], i[0]+i[2])])
    df_dict[key] = pd.DataFrame({
        first_colname: source_list,
        second_colname: dest_list
    })

print(df_dict)

first_df = list(df_dict.values())[0]
print(first_df.shape)
for seed in seeds[0]:
    if (seed in first_df["seed"]):
        print(seed)
        first_df = pd.concat([
            first_df,
            pd.DataFrame({"seed": [seed], "soil": [seed]})],
            ignore_index=True
        )
        
print(first_df)
print(first_df.shape)

first_df = first_df.drop_duplicates("seed")
print(first_df.shape)


remaining_dfs = list(df_dict.values())[1:]
    
combined_df = first_df.copy()
for i in remaining_dfs:
    combined_df = combined_df.merge(
        i,
        how = "left"
    )
    combined_df.iloc[:, -1] = np.where(
        combined_df.iloc[:, -1].isna(),
        combined_df.iloc[:, -2],
        combined_df.iloc[:, -1]
    )
print(combined_df)
print(combined_df.shape)

asdf = [x in first["seed"] for x in seeds[0]]
print(asdf)

seeds_only = combined_df.loc[combined_df["seed"].isin(seeds[0])]

seeds_only