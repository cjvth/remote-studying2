let changed = {}
let original = {}
let count_new = 0


function update_t(clicked_id) {
    let t_id = clicked_id.split('-')[0]
    let butt = clicked_id.split('-')[1]
    if (butt === 'edit') {
        let _name = document.getElementById(t_id + '-name').innerText
        let _info = document.getElementById(t_id + '-info').innerText
        let tr = document.getElementById(t_id + '-tr')
        tr.innerHTML = ''

        let td = document.createElement("td")
        tr.appendChild(td)
        let name = document.createElement("input")
        name = Object.assign(name, {
            id: t_id + '-name', type: 'text',
            className: 'form-control', value: _name, placeholder: 'Имя'
        })
        name.style.fontWeight = "bold"
        td.appendChild(name)
        let info = document.createElement("textarea")
        info = Object.assign(info, {
            id: t_id + '-info', rows: 4, className: 'form-control',
            value: _info, placeholder: 'Информация'
        })
        td.appendChild(info)

        td = document.createElement("td")
        tr.appendChild(td)
        td.className = "flexi-butt"
        let save = document.createElement("button")
        save = Object.assign(save, {
            id: t_id + '-save',
            className: 'btn btn-success', innerText: 'Сохранить'
        })
        save.onclick = function () {
            update_t(this.id)
        }
        td.appendChild(save)
        let cancel = document.createElement("button")
        cancel = Object.assign(cancel, {
            id: t_id + '-cancel',
            className: 'btn btn-secondary', innerText: 'Отменить'
        })
        cancel.onclick = function () {
            update_t(this.id)
        }
        td.appendChild(cancel)
        if (typeof original[t_id] !== "undefined" && t_id[0] !== '_') {
            original[t_id] = {'name': _name, 'info': _info}
        }
        changed[t_id] = {'type': 'editing', 'name': _name, 'info': _info}

    } else if (butt === 'save') {
        let _name = document.getElementById(t_id + '-name').value
        let _info = document.getElementById(t_id + '-info').value
        let tr = document.getElementById(t_id + '-tr')
        tr.innerHTML = ''

        let td = document.createElement("td")
        tr.appendChild(td)
        let name = document.createElement("h4")
        name = Object.assign(name, {id: t_id + '-name', innerHTML: _name})
        td.appendChild(name)
        let info = document.createElement("p")
        info = Object.assign(info, {
            id: t_id + '-info',
            innerText: _info
        })
        td.appendChild(info)

        td = document.createElement("td")
        tr.appendChild(td)
        td.className = "flexi-butt"
        let edit = document.createElement("button")
        edit = Object.assign(edit, {
            id: t_id + '-edit',
            className: 'btn btn-warning', innerText: 'Изменить'
        })
        edit.onclick = function () {
            update_t(this.id)
        }
        td.appendChild(edit)
        let del = document.createElement("button")
        del = Object.assign(del, {
            id: t_id + '-delete',
            className: 'btn btn-danger', innerText: 'Удалить'
        })
        del.onclick = function () {
            update_t(this.id)
        }
        td.appendChild(del)
        changed[t_id] = {'action': 'edited', 'name': _name, 'info': _info}

    } else if (butt === 'delete') {

        let _name = document.getElementById(t_id + '-name').innerText
        let _info = document.getElementById(t_id + '-info').innerText
        let tr = document.getElementById(t_id + '-tr')
        tr.innerHTML = ''

        let td = document.createElement("td")
        tr.appendChild(td)
        let name = document.createElement("h4")
        name = Object.assign(name, {id: t_id + '-name', innerHTML: _name})
        name.style.color = "#AAAAAA"
        td.appendChild(name)

        td = document.createElement("td")
        tr.appendChild(td)
        td.className = "flexi-butt"
        let cancel = document.createElement("button")
        cancel = Object.assign(cancel, {
            id: t_id + '-cancel',
            className: 'btn btn-secondary', innerText: 'Отменить'
        })
        cancel.onclick = function () {
            update_t(this.id)
        }
        td.appendChild(cancel)
        if (typeof original[t_id] !== "undefined" && t_id[0] !== '_') {
            original[t_id] = {'name': _name, 'info': _info}
        }
        changed[t_id] = {'action': 'deleted', 'name': _name, 'info': _info}

    } else if (butt === 'cancel') {

        let _name = changed[t_id].name
        let _info = changed[t_id].info
        let tr = document.getElementById(t_id + '-tr')
        tr.innerHTML = ''

        let td = document.createElement("td")
        tr.appendChild(td)
        let name = document.createElement("h4")
        name = Object.assign(name, {id: t_id + '-name', innerHTML: _name})
        td.appendChild(name)
        let info = document.createElement("p")
        info = Object.assign(info, {
            id: t_id + '-info',
            innerText: _info
        })
        td.appendChild(info)

        td = document.createElement("td")
        tr.appendChild(td)
        td.className = "flexi-butt"
        let edit = document.createElement("button")
        edit = Object.assign(edit, {
            id: t_id + '-edit',
            className: 'btn btn-warning', innerText: 'Изменить'
        })
        edit.onclick = function () {
            update_t(this.id)
        }
        td.appendChild(edit)
        let del = document.createElement("button")
        del = Object.assign(del, {
            id: t_id + '-delete',
            className: 'btn btn-danger', innerText: 'Удалить'
        })
        del.onclick = function () {
            update_t(this.id)
        }
        td.appendChild(del)
        delete changed[t_id]
    }
}

function new_t() {
    let n = '_' + (++count_new).toString()
    let div = document.getElementById('teachers')
    let border = document.createElement('div')
    border = Object.assign(border, {id: n, className: 'col-md6 border rounded'})
    div.insertAdjacentElement("afterbegin", border)
    let table = document.createElement('table')
    table.style.width = "100%"
    border.appendChild(table)
    let tr = document.createElement('tr')
    tr.id = n + '-tr'
    table.appendChild(tr)
    changed[n] = {'type': 'created', 'name': '', 'info': ''}
    update_t(n + '-cancel')
    update_t(n + '-edit')
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