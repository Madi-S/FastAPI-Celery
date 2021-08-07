;(function () {
    console.log('Sanity Check!')
})()

function handleClick(task_delay) {
    fetch('/tasks', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ delay: task_delay })
    })
        .then(response => response.json())
        .then(task => getStatus(task.id))
}

function getStatus(taskID) {
    fetch(`/tasks/${taskID}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(task => {
            console.log(task)
            const html = `
      <tr>
        <td>${taskID}</td>
        <td>${task.status}</td>
        <td>${task.result}</td>
      </tr>`
            const newRow = document.getElementById('tasks').insertRow(0)
            newRow.innerHTML = html

            if (task.status === 'SUCCESS' || task.status === 'FAILURE')
                return false
            setTimeout(function () {
                getStatus(task.id)
            }, 1000)
        })
        .catch(err => console.log(err))
}
