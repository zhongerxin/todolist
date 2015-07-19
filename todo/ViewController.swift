//
//  ViewController.swift
//  todo
//
//  Created by 钟信 on 15/7/19.
//  Copyright (c) 2015年 zhongxin. All rights reserved.
//

import UIKit

var todos: [TodoModel] = []
func dateFromString(dateStr:String) -> NSDate? {
    let dateFormatter = NSDateFormatter()
    dateFormatter.dateFormat="yyyy-MM-dd"
    let date = dateFormatter.dateFromString(dateStr)
    return date
    
}

class ViewController: UIViewController, UITableViewDataSource, UITableViewDelegate {
    @IBOutlet weak var tableView: UITableView!

    override func viewDidLoad() {
        super.viewDidLoad()
        // Do any additional setup after loading the view, typically from a nib.
        todos = [TodoModel(id: "1", image: "child-selected", title: "1.去游乐场", date: dateFromString("2014-11-2")!),
                TodoModel(id: "2", image: "shopping-cart-selected", title: "2.购物", date: dateFromString("2014-10-2")!),
            TodoModel(id: "3", image: "phone-selected", title: "3.打电话", date: dateFromString("2015-11-2")!),
            TodoModel(id: "4", image: "travel-selected", title: "4.去欧洲旅游", date: dateFromString("2015-9-2")!)]
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }

    
    func tableView(tableView: UITableView, numberOfRowsInSection section: Int) -> Int {
        return todos.count
    }
    
    
    func tableView(tableView: UITableView, cellForRowAtIndexPath indexPath: NSIndexPath) -> UITableViewCell {

            let cell = self.tableView.dequeueReusableCellWithIdentifier("todoCell") as!  UITableViewCell
        var todo = todos[indexPath.row] as TodoModel
        var image = cell.viewWithTag(101) as! UIImageView
        var title = cell.viewWithTag(102) as! UILabel
        var date = cell.viewWithTag(103) as! UILabel
        image.image = UIImage(named: todo.image)

        return cell
        
        
    }
}

