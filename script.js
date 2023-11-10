const apiUrl = "http://127.0.0.1:8000/todos";

// 할 일 목록을 불러와서 화면에 표시
async function fetchTodos() {
  const response = await fetch(apiUrl);
  const data = await response.json();
  const list = document.getElementById("todo-list");
  list.innerHTML = ""; // 목록 초기화
  data.todos.forEach((todo) => {
    const li = document.createElement("li");
    li.textContent = todo.content;
    li.setAttribute("data-todo-id", todo.todo_id); // li 요소에 data-todo-id 속성 추가

    //삭제 버튼 추가
    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "❌";
    deleteBtn.classList.add("delete-btn");
    deleteBtn.onclick = () => deleteTodoElement(todo.todo_id); // 삭제 함수 연결
    li.appendChild(deleteBtn);

    list.appendChild(li);
  });
}

// 할 일을 삭제
async function deleteTodoElement(todoId) {
  try {
    await fetch(`${apiUrl}/${todoId}`, {
      method: "DELETE",
    });
    const todoItem = document.querySelector(`li[data-todo-id]="&{todoId}"`);
    if (todoItem) {
      todoItem.remove(); // DOM에서 해당 항목 제거
    }
  } catch (error) {
    console.error("Error:", error);
  }
  fetchTodos();
}

// submit버튼 눌리면 새 할 일을 서버에 추가
document.getElementById("todo-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const content = document.getElementById("todo-content").value;
  await fetch(apiUrl, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content: content, is_done: false }),
  });
  document.getElementById("todo-content").value = ""; // 입력 필드 초기화
  fetchTodos(); // 목록 갱신
});

// 페이지가 로드될 때 할 일 목록을 불러옴
window.onload = fetchTodos;
