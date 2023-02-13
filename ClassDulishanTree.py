class DulishanTrees :
    def __init__(self, tree_name) :
        self.tree_name = tree_name
        self.longitude = []
        self.latitude = []
        self.nums = []

    def add(self, lgd, ltd, num) :
        self.longitude.append(lgd)
        self.latitude.append(ltd)
        self.nums.append(num)

def get_data_pd(file_name) :
    #file_name = '*.txt'
    import pandas as pd
    all_trees = {}
    tree_data = pd.read_csv(file_name, encoding='utf-8')
    for i in range(len(tree_data)) :
        if tree_data['樹種'][i] not in all_trees :
            all_trees[tree_data['樹種'][i]] = DulishanTrees(tree_data['樹種'][i])
        all_trees[tree_data['樹種'][i]].add(tree_data['經度'][i], tree_data['緯度'][i], tree_data['數量'][i])
    return all_trees

def get_data_re(file_name) :
    #file_name = '*.txt'
    import re
    all_trees = {}
    patt = re.compile(r'(\w+),(\d+\.\d+),(\d+\.\d+),(\d+),(\S+)\n')
    with open(file_name,'r',encoding='utf-8') as f :
        for line in f :
            ma = re.search(patt, line)
            if ma :
                if ma[1] not in all_trees :
                    all_trees[ma[1]] = DulishanTrees(ma[1])
                all_trees[ma[1]].add(float(ma[2]), float(ma[3]), int(ma[4]))
    return all_trees

def write_tree_fmap_from_dict(tree_data, tree_name, file_name) :
    #type(tree_data) = <class 'dict'>, type(tree_name) = <class 'str'>
    #file_name = '*.html'
    import folium
    from folium.plugins import MarkerCluster
    c_lng = round(sum(tree_data[tree_name].longitude)/len(tree_data[tree_name].longitude),4)
    c_lat = round(sum(tree_data[tree_name].latitude)/len(tree_data[tree_name].latitude),4)
    fmap = folium.Map(location=[c_lat, c_lng], zoom_start=11)
    cluster_trees = MarkerCluster().add_to(fmap)
    for lng, lat, num in zip(tree_data[tree_name].longitude, tree_data[tree_name].latitude, tree_data[tree_name].nums) :
        co = 0
        while co < num :
            co += 1
            folium.Marker(
                location=[lat, lng],
                icon = None,
                popup = tree_name,
                ).add_to(cluster_trees)
    fmap.add_child(cluster_trees)
    fmap.save(file_name)

if __name__ == "__main__" :
    tdata = get_data_re('tree_atri_id_u8.txt')
    write_tree_fmap_from_dict(tdata, '櫻花', 'sak.html')
