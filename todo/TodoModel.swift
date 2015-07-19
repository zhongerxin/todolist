//
//  TodoModel.swift
//  todo
//
//  Created by 钟信 on 15/7/19.
//  Copyright (c) 2015年 zhongxin. All rights reserved.
//

import UIKit

class TodoModel: NSObject {
    var id: String
    var image: String
    var title: String
    var date: NSDate
    
    init (id: String, image: String, title: String, date: NSDate) {
        self.id = id
        self.title = title
        self.image = image
        self.date = date
    }
}