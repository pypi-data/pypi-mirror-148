This project is an util package to create a crawler.
It contains many tools which can finish part function.
There is an example:


from PaperCrawlerUtil import util as u
import os
import time


for times in ["2019", "2020", "2021"]:
    if os.path.exists("CVPR_{}".format(times)):
        print("文件夹存在")
    else:
        os.makedirs("CVPR_{}".format(times))
    html = u.random_proxy_header_access("https://openaccess.thecvf.com/CVPR{}".format(times), require_proxy=False)
    attr_list = u.get_attribute_of_html(html, {'href': "in", 'CVPR': "in", "py": "in", "day": "in"})
    for ele in attr_list:
        path = ele.split("<a href=\"")[1].split("\">")[0]
        path = "https://openaccess.thecvf.com/" + path
        html = u.random_proxy_header_access(path)
        attr_list = u.get_attribute_of_html(html,
                                          {'href': "in", 'CVPR': "in", "content": "in", "papers": "in"})
        for eles in attr_list:
            pdf_path = eles.split("<a href=\"")[1].split("\">")[0]
            dir = os.path.abspath("CVPR_{}".format(times))
            work_path = os.path.join(dir, '{}.pdf').format(str(time.strftime("%H_%M_%S", time.localtime())))
            u.retrieve_file("https://openaccess.thecvf.com/" + pdf_path, work_path)

