var changed = new Set()


function update_t(clicked_id) {
    let t_id = clicked_id.split('-')[0]
    let butt = clicked_id.split('-')[1]
    if (butt === 'edit') {
        let _name = document.getElementById(t_id + '-name').innerText
        let _info = document.getElementById(t_id + '-info').innerText
        // let div = document.getElementById(t_id)
        // div.innerHTML = ''
        // let table = document.createElement("table")
        // div.appendChild(table)
        // let tr = document.createElement("tr")
        // table.appendChild(tr)

        let tr = document.getElementById(t_id + '-tr')
        tr.innerHTML = ''
        let td = document.createElement("td")
        // td.style = "width: 100%"
        tr.appendChild(td)
        let name = document.createElement("input")
        name.id = t_id + '-name'
        name.type = 'text'
        name.className = "form-control"
        name.value = _name
        name.placeholder = 'Имя'
        td.appendChild(name)
        let info = document.createElement("textarea")
        info.id = t_id + '-info'
        info.className = "form-control"
        info.textContent = _info
        info.placeholder = 'Информация'
        td.appendChild(info)

    }
}


function send_t() {
    let req = new XMLHttpRequest();
    let result = document.getElementById(clicked_id);
    req.onreadystatechange = function () {
        console.log(this.readyState + ' ' + this.status + ' ' + this.responseText)
        if (this.readyState === 4) {
            if (this.status === 200)
                result.innerHTML = this.responseText;
            else
                result.innerHTML = 'Error ' + this.status + ': ' + this.statusText;
        }
    }

    req.open('POST', '/update_db', true);
    let body = {
        'name': document.getElementById('name').innerText,
        'sas': 123
    }
    req.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    req.send(JSON.stringify(body));
    // req.setRequestHeader('content-type', 'application/x-www-form-urlencoded;charset=UTF-8');
    // req.send("name=" + document.getElementById('name').value + '&sas=123');
}