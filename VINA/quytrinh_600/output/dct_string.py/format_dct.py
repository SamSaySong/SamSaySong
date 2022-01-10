dct_All = []

dct_table = { "Bước": "",
        "Tên cơ quan": "",
        "Phòng ban xử lý": "",
        "Thời gian gửi":"",
        "Trạng thái hồ sơ":"",
        "Desc": []         
    }
dict_con = {
            "STT": [],
            "Cán bộ xử lý":[],
            "Hành động": [],
            "Thời gian xử lý":[],
            }

dct_data_1 = [{
    "Bước": "1", 
    "Tên cơ quan": "BHXH Tp. Hồ Chí Minh", 
    "Phòng ban xử lý": "Phòng Tiếp nhận và trả kết quả TTHC", 
    "Thời gian gửi": "22/11/2021 09:57", 
    "Trạng thái hồ sơ": "Còn 0 ngày 5 giờ 15 phút", 
    "Desc": [
        {"STT": ["1", "2", "3", "4","5"],
        "Cán bộ xử lý": ["Hệ thống tự động", "Lê Thị Diện", "Lê Thị Diện", "Nguyễn Thị Thanh Lệ"], 
        "Hành động": ["Nhận hồ sơ điện tử", "Phân công", "Tiếp nhận", "Xử lý (Hồ sơ hợp lệ)", "Phân công"], 
        "Thời gian xử lý": ["22/11/2021 09:57", "24/11/2021 14:39", "24/11/2021 14:39", "25/11/2021 08:24","24/11/2021 14:39"]
        }
        ]
},
{
    "Bước": "2", 
    "Tên cơ quan": "BHXH Tp. Hồ Chí Minh", 
    "Phòng ban xử lý": "Phòng Tiếp nhận và trả kết quả TTHC", 
    "Thời gian gửi": "22/11/2021 09:57", 
    "Trạng thái hồ sơ": "Còn 0 ngày 5 giờ 15 phút", 
    "Desc": [
        {"STT": ["1", "2", "3", "4", "5"], 
        "Cán bộ xử lý": ["Hệ thống tự động", "Lê Thị Diện", "Lê Thị Diện", "Nguyễn Thị Thanh Lệ", "Lê Thị Diện"],
        "Hành động": ["Nhận hồ sơ điện tử", "Phân công", "Tiếp nhận", "Xử lý (Hồ sơ hợp lệ)", "Phân công"], 
        "Thời gian xử lý": ["22/11/2021 09:57", "24/11/2021 14:39", "24/11/2021 14:39", "25/11/2021 08:24", "24/11/2021 14:30"]
        }
    ]
},{
    "Bước": "3", 
    "Tên cơ quan": "BHXH Tp. Hồ Chí Minh", 
    "Phòng ban xử lý": "Phòng Tiếp nhận và trả kết quả TTHC", 
    "Thời gian gửi": "22/11/2021 09:57", 
    "Trạng thái hồ sơ": "Còn 0 ngày 5 giờ 15 phút", 
    "Desc": [
        {"STT": ["1", "2", "3", "4"], 
        "Cán bộ xử lý": ["Hệ thống tự động", "Lê Thị Diện", "Lê Thị Diện", "Nguyễn Thị Thanh Lệ"],
        "Hành động": ["Nhận hồ sơ điện tử", "Phân công", "Tiếp nhận", "Xử lý (Hồ sơ hợp lệ)"], 
        "Thời gian xử lý": ["22/11/2021 09:57", "24/11/2021 14:39", "24/11/2021 14:39", "25/11/2021 08:24"]
        }
    ]
}
]

dct_data_2 = [{
    "Bước": "1", 
    "Tên cơ quan": "BHXH Tp. Hồ Chí Minh", 
    "Phòng ban xử lý": "Phòng Tiếp nhận và trả kết quả TTHC", 
    "Thời gian gửi": "22/11/2021 09:57", 
    "Trạng thái hồ sơ": "Còn 0 ngày 5 giờ 15 phút", 
    "Desc": [
        {"STT": ["1", "2", "3", "4", "5"], 
        "Cán bộ xử lý": ["Hệ thống tự động", "Lê Thị Diện", "Lê Thị Diện", "Nguyễn Thị Thanh Lệ", "Lê Thị Diện"],
        "Hành động": ["Nhận hồ sơ điện tử", "Phân công", "Tiếp nhận", "Xử lý (Hồ sơ hợp lệ)", "Phân công"], 
        "Thời gian xử lý": ["22/11/2021 09:57", "24/11/2021 14:39", "24/11/2021 14:39", "25/11/2021 08:24", "24/11/2021 14:39"]
        }
    ]
},
{
    "Bước": "2", 
    "Tên cơ quan": "BHXH Tp. Hồ Chí Minh", 
    "Phòng ban xử lý": "Phòng Tiếp nhận và trả kết quả TTHC", 
    "Thời gian gửi": "22/11/2021 09:57", 
    "Trạng thái hồ sơ": "Còn 0 ngày 5 giờ 15 phút", 
    "Desc": [
        {"STT": ["1", "2", "3", "4", "5"], 
        "Cán bộ xử lý": ["Hệ thống tự động", "Lê Thị Diện", "Lê Thị Diện", "Nguyễn Thị Thanh Lệ", "Lê Thị Diện"],
        "Hành động": ["Nhận hồ sơ điện tử", "Phân công", "Tiếp nhận", "Xử lý (Hồ sơ hợp lệ)", "Phân công"], 
        "Thời gian xử lý": ["22/11/2021 09:57", "24/11/2021 14:39", "24/11/2021 14:39", "25/11/2021 08:24", "24/11/2021 14:39"]
        }
    ]
},{
    "Bước": "3",
    "Tên cơ quan": "BHXH Tp. Hồ Chí Minh", 
    "Phòng ban xử lý": "Phòng Tiếp nhận và trả kết quả TTHC", 
    "Thời gian gửi": "22/11/2021 09:57", 
    "Trạng thái hồ sơ": "Còn 0 ngày 5 giờ 15 phút", 
    "Desc": [
        {"STT": ["1", "2", "3", "4", "5"], 
        "Cán bộ xử lý": ["Hệ thống tự động", "Lê Thị Diện", "Lê Thị Diện", "Nguyễn Thị Thanh Lệ", "Lê Thị Diện"],
        "Hành động": ["Nhận hồ sơ điện tử", "Phân công", "Tiếp nhận", "Xử lý (Hồ sơ hợp lệ)", "Phân công"], 
        "Thời gian xử lý": ["22/11/2021 09:57", "24/11/2021 14:39", "24/11/2021 14:39", "25/11/2021 08:24", "24/11/2021 14:39"]
        }
    ]
}
]


def compile_data(dct_data_1, dct_data_2):


    for idx_dct, j_dct in enumerate(dct_data_2):

       

        if len(dct_data_1[idx_dct]['Desc'][0]['STT']) < len(dct_data_2[idx_dct]['Desc'][0]['STT']):
            dct_All.append("Bước: "+dct_data_2[idx_dct]['Bước']+" | "+"Desc: "+'STT: '+dct_data_2[idx_dct]['Desc'][0]['STT'][-1]+" | ")
            dct_All.append('Cán bộ xử lý: '+ dct_data_2[idx_dct]['Desc'][0]['Cán bộ xử lý'][-1]+" | ")
            dct_All.append('Hành động: '+ dct_data_2[idx_dct]['Desc'][0]['Hành động'][-1]+" | ")
            dct_All.append('Thời gian xử lý: '+ dct_data_2[idx_dct]['Desc'][0]['Thời gian xử lý'][-1])
            dct_All.append("\n")

        elif len(dct_data_1[idx_dct]['Desc'][0]['STT']) == len(dct_data_2[idx_dct]['Desc'][0]['STT']):

            for idx, i in enumerate(dct_data_1[idx_dct]['Desc'][0]['Cán bộ xử lý']) :

                if i != dct_data_2[idx_dct]['Desc'][0]['Cán bộ xử lý'][idx]:
                    dct_All.append("Bước: "+dct_data_2[idx_dct]['Bước']+" | "+dct_data_2[idx_dct]['Desc'][0]['Cán bộ xử lý'][idx])
                    dct_All.append('Cán bộ xử lý: '+ dct_data_2[idx_dct]['Desc'][0]['Cán bộ xử lý'][-1]+" | ")
                    dct_All.append('Hành động: '+ dct_data_2[idx_dct]['Desc'][0]['Hành động'][-1]+" | ")
                    dct_All.append('Thời gian xử lý: '+ dct_data_2[idx_dct]['Desc'][0]['Thời gian xử lý'][-1])
                    dct_All.append("\n")

            for idx, i in enumerate(dct_data_1[idx_dct]['Desc'][0]['Hành động']) :

                if i != dct_data_2[idx_dct]['Desc'][0]['Hành động'][idx]:
          
                    dct_All.append("Bước: "+dct_data_2[idx_dct]['Bước']+" | "+"Desc: "+'STT: '+dct_data_2[idx_dct]['Desc'][0]['STT'][-1]+" | ")
                    dct_All.append('Cán bộ xử lý: '+ dct_data_2[idx_dct]['Desc'][0]['Cán bộ xử lý'][-1]+" | ")
                    dct_All.append('Hành động: '+ dct_data_2[idx_dct]['Desc'][0]['Hành động'][-1]+" | ")
                    dct_All.append('Thời gian xử lý: '+ dct_data_2[idx_dct]['Desc'][0]['Thời gian xử lý'][-1])
                    dct_All.append("\n")

            for idx, i in enumerate(dct_data_1[idx_dct]['Desc'][0]['Thời gian xử lý']) :

                if i != dct_data_2[idx_dct]['Desc'][0]['Thời gian xử lý'][idx]:
                    dct_All.append("Bước: "+dct_data_2[idx_dct]['Bước']+"|"+"Desc: "+'STT: '+dct_data_2[idx_dct]['Desc'][0]['STT'][-1]+" | ")
                    dct_All.append('Cán bộ xử lý: '+ dct_data_2[idx_dct]['Desc'][0]['Cán bộ xử lý'][-1]+" | ")
                    dct_All.append('Hành động: '+ dct_data_2[idx_dct]['Desc'][0]['Hành động'][-1]+" | ")
                    dct_All.append('Thời gian xử lý: '+ dct_data_2[idx_dct]['Desc'][0]['Thời gian xử lý'][-1])
                    dct_All.append("\n")

            


    return dct_All    
    


a = compile_data(dct_data_1, dct_data_2)

print("".join(a))
