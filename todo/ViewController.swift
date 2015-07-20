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
        todos = []
        
        navigationItem.leftBarButtonItem = editButtonItem()
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
        title.text = todo.title
        let locale = NSLocale.autoupdatingCurrentLocale()
        let dateFormat = NSDateFormatter.dateFormatFromTemplate("yyyy-MM-dd", options:0, locale:locale)
        let dateFormatter = NSDateFormatter()
        dateFormatter.dateFormat = dateFormat
        date.text = dateFormatter.stringFromDate(todo.date)

        return cell
        
        
    }
    
    func tableView(tableView: UITableView, commitEditingStyle editingStyle: UITableViewCellEditingStyle, forRowAtIndexPath indexPath: NSIndexPath) {
        if editingStyle == UITableViewCellEditingStyle.Delete {
            todos.removeAtIndex(indexPath.row)
            self.tableView.deleteRowsAtIndexPaths([indexPath], withRowAnimation: UITableViewRowAnimation.Automatic)
        }
    }
    //edit mode
    override func setEditing(editing: Bool, animated: Bool) {
        super.setEditing(editing, animated: animated)
        self.tableView.setEditing(editing, animated: animated)
    }
    @IBAction func close(segue:UIStoryboardSegue) {
        println("closed")
        tableView.reloadData()
    }
}

