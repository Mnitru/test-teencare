import { useState, useEffect } from 'react';

function App() {
  const API = 'http://localhost:8000';
  
  const [parents, setParents] = useState([]);
  const [students, setStudents] = useState([]);
  const [classes, setClasses] = useState([]);
  const [registrations, setRegistrations] = useState([]);
  const [selectedDay, setSelectedDay] = useState('Monday');

  // Form states
  const [newParent, setNewParent] = useState({ name: '', phone: '', email: '' });
  const [newStudent, setNewStudent] = useState({
    name: '', dob: '2015-01-01', gender: 'Male', current_grade: 6, parent_id: 1
  });
  const [newClass, setNewClass] = useState({
    name: '', subject: '', day_of_week: 'Monday', time_slot: '08:00-09:00',
    teacher_name: '', max_students: 15
  });
  const [newSub, setNewSub] = useState({
    student_id: 1, package_name: 'Basic', start_date: '2025-04-01',
    end_date: '2025-06-30', total_sessions: 20
  });

  const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'];

  const loadAll = async () => {
    // Load parents, students, classes
    const pRes = await fetch(`${API}/api/parents`);
    if (pRes.ok) setParents(await pRes.json());

    const sRes = await fetch(`${API}/api/students`);
    if (sRes.ok) setStudents(await sRes.json());

    const cRes = await fetch(`${API}/api/classes?day=${selectedDay}`);
    if (cRes.ok) setClasses(await cRes.json());

    // Load registrations
    const rRes = await fetch(`${API}/api/registrations`);
    if (rRes.ok) setRegistrations(await rRes.json());
  };

  useEffect(() => {
    loadAll();
  }, [selectedDay]);

  // Tạo Parent
  const createParent = async (e) => {
    e.preventDefault();
    const res = await fetch(`${API}/api/parents`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newParent)
    });
    if (res.ok) {
      alert('Tạo phụ huynh thành công!');
      setNewParent({ name: '', phone: '', email: '' });
      loadAll();
    }
  };

  // Tạo Student
  const createStudent = async (e) => {
    e.preventDefault();
    const res = await fetch(`${API}/api/students`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newStudent)
    });
    if (res.ok) {
      alert('Tạo học sinh thành công!');
      setNewStudent({ name: '', dob: '2015-01-01', gender: 'Male', current_grade: 6, parent_id: 1 });
      loadAll();
    }
  };

  // Tạo Class
  const createClass = async (e) => {
    e.preventDefault();
    const res = await fetch(`${API}/api/classes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newClass)
    });
    if (res.ok) {
      alert('Tạo lớp học thành công!');
      setNewClass({ name: '', subject: '', day_of_week: 'Monday', time_slot: '08:00-09:00', teacher_name: '', max_students: 15 });
      loadAll();
    }
  };

  // Tạo Subscription
  const createSubscription = async (e) => {
    e.preventDefault();
    const res = await fetch(`${API}/api/subscriptions`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newSub)
    });
    if (res.ok) {
      alert('Tạo gói học thành công!');
      loadAll();
    }
  };

  // Đăng ký học sinh vào lớp
  const registerStudent = async (classId, studentId) => {
    const res = await fetch(`${API}/api/classes/${classId}/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ student_id: studentId })
    });
    const data = await res.json();
    if (res.ok) {
      alert('Đăng ký thành công!');
      loadAll();
    } else {
      alert(data.detail || 'Đăng ký thất bại');
    }
  };

  // Hủy đăng ký
  const cancelRegistration = async (regId) => {
    if (!window.confirm('Bạn chắc chắn muốn hủy đăng ký này?')) return;
    const res = await fetch(`${API}/api/registrations/${regId}`, { method: 'DELETE' });
    if (res.ok) {
      alert('Đã hủy đăng ký và hoàn buổi!');
      loadAll();
    } else {
      alert('Hủy thất bại');
    }
  };

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif', maxWidth: '1200px', margin: '0 auto' }}>
      <h1>TeenUp Mini LMS</h1>

      {/* Các form tạo (giữ nguyên như trước) */}
      <div style={{ marginBottom: '30px', border: '1px solid #ddd', padding: '15px', borderRadius: '8px' }}>
        <h2>Tạo Phụ huynh</h2>
        <form onSubmit={createParent} style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <input placeholder="Tên phụ huynh" value={newParent.name} onChange={e => setNewParent({ ...newParent, name: e.target.value })} required />
          <input placeholder="Số điện thoại" value={newParent.phone} onChange={e => setNewParent({ ...newParent, phone: e.target.value })} required />
          <input placeholder="Email" type="email" value={newParent.email} onChange={e => setNewParent({ ...newParent, email: e.target.value })} required />
          <button type="submit" style={{ background: '#f97316', color: 'white', padding: '8px 16px', border: 'none', borderRadius: '4px' }}>Tạo Parent</button>
        </form>
      </div>

      <div style={{ marginBottom: '30px', border: '1px solid #ddd', padding: '15px', borderRadius: '8px' }}>
        <h2>Tạo Học sinh</h2>
        <form onSubmit={createStudent} style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <input placeholder="Tên học sinh" value={newStudent.name} onChange={e => setNewStudent({ ...newStudent, name: e.target.value })} required />
          <input type="date" value={newStudent.dob} onChange={e => setNewStudent({ ...newStudent, dob: e.target.value })} />
          <select value={newStudent.gender} onChange={e => setNewStudent({ ...newStudent, gender: e.target.value })}>
            <option>Male</option>
            <option>Female</option>
          </select>
          <input type="number" placeholder="Lớp hiện tại" value={newStudent.current_grade} onChange={e => setNewStudent({ ...newStudent, current_grade: parseInt(e.target.value) })} />
          <input type="number" placeholder="Parent ID" value={newStudent.parent_id} onChange={e => setNewStudent({ ...newStudent, parent_id: parseInt(e.target.value) })} />
          <button type="submit" style={{ background: '#f97316', color: 'white', padding: '8px 16px', border: 'none', borderRadius: '4px' }}>Tạo Student</button>
        </form>
      </div>

      <div style={{ marginBottom: '30px', border: '1px solid #ddd', padding: '15px', borderRadius: '8px' }}>
        <h2>Tạo Lớp học</h2>
        <form onSubmit={createClass} style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <input placeholder="Tên lớp" value={newClass.name} onChange={e => setNewClass({ ...newClass, name: e.target.value })} required />
          <input placeholder="Môn học" value={newClass.subject} onChange={e => setNewClass({ ...newClass, subject: e.target.value })} required />
          <select value={newClass.day_of_week} onChange={e => setNewClass({ ...newClass, day_of_week: e.target.value })}>
            {days.map(d => <option key={d} value={d}>{d}</option>)}
          </select>
          <input placeholder="Khung giờ" value={newClass.time_slot} onChange={e => setNewClass({ ...newClass, time_slot: e.target.value })} required />
          <input placeholder="Giáo viên" value={newClass.teacher_name} onChange={e => setNewClass({ ...newClass, teacher_name: e.target.value })} required />
          <input type="number" placeholder="Sĩ số tối đa" value={newClass.max_students} onChange={e => setNewClass({ ...newClass, max_students: parseInt(e.target.value) })} />
          <button type="submit" style={{ background: '#f97316', color: 'white', padding: '8px 16px', border: 'none', borderRadius: '4px' }}>Tạo Class</button>
        </form>
      </div>

      <div style={{ marginBottom: '30px', border: '1px solid #ddd', padding: '15px', borderRadius: '8px' }}>
        <h2>Tạo Gói học (Subscription)</h2>
        <form onSubmit={createSubscription} style={{ display: 'flex', gap: '10px', flexWrap: 'wrap' }}>
          <input type="number" placeholder="Student ID" value={newSub.student_id} onChange={e => setNewSub({ ...newSub, student_id: parseInt(e.target.value) })} />
          <input placeholder="Tên gói" value={newSub.package_name} onChange={e => setNewSub({ ...newSub, package_name: e.target.value })} />
          <input type="date" value={newSub.start_date} onChange={e => setNewSub({ ...newSub, start_date: e.target.value })} />
          <input type="date" value={newSub.end_date} onChange={e => setNewSub({ ...newSub, end_date: e.target.value })} />
          <input type="number" placeholder="Tổng buổi" value={newSub.total_sessions} onChange={e => setNewSub({ ...newSub, total_sessions: parseInt(e.target.value) })} />
          <button type="submit" style={{ background: '#f97316', color: 'white', padding: '8px 16px', border: 'none', borderRadius: '4px' }}>Tạo Subscription</button>
        </form>
      </div>

      {/* Danh sách lớp học theo tuần */}
      <h2>Danh sách lớp học theo ngày</h2>
      <div style={{ display: 'flex', gap: '5px', marginBottom: '15px', flexWrap: 'wrap' }}>
        {days.map(day => (
          <button
            key={day}
            onClick={() => setSelectedDay(day)}
            style={{
              padding: '8px 16px',
              background: selectedDay === day ? '#f97316' : '#ddd',
              color: selectedDay === day ? 'white' : 'black',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            {day}
          </button>
        ))}
      </div>

      <table border="1" style={{ width: '100%', borderCollapse: 'collapse', marginBottom: '40px' }}>
        <thead>
          <tr style={{ background: '#f97316', color: 'white' }}>
            <th style={{ padding: '10px' }}>Tên lớp</th>
            <th>Môn</th>
            <th>Khung giờ</th>
            <th>Giáo viên</th>
            <th>Sĩ số</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          {classes.map(cls => (
            <tr key={cls.id}>
              <td style={{ padding: '10px' }}>{cls.name}</td>
              <td>{cls.subject}</td>
              <td>{cls.time_slot}</td>
              <td>{cls.teacher_name}</td>
              <td>{cls.max_students}</td>
              <td>
                <select id={`student-${cls.id}`} style={{ marginRight: '5px' }}>
                  {students.map(s => <option key={s.id} value={s.id}>{s.name}</option>)}
                </select>
                <button
                  onClick={() => {
                    const studentId = parseInt(document.getElementById(`student-${cls.id}`).value);
                    registerStudent(cls.id, studentId);
                  }}
                  style={{ background: '#10b981', color: 'white', padding: '4px 12px', border: 'none', borderRadius: '4px' }}
                >
                  Đăng ký
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      {/* === BẢNG ĐĂNG KÝ HIỆN TẠI + NÚT HỦY === */}
      <h2>Các đăng ký hiện tại</h2>
      <table border="1" style={{ width: '100%', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ background: '#f97316', color: 'white' }}>
            <th style={{ padding: '10px' }}>Học sinh</th>
            <th>Lớp học</th>
            <th>Hành động</th>
          </tr>
        </thead>
        <tbody>
          {registrations.map(reg => (
            <tr key={reg.id}>
              <td style={{ padding: '10px' }}>{reg.student_name}</td>
              <td>{reg.class_name}</td>
              <td>
                <button
                  onClick={() => cancelRegistration(reg.id)}
                  style={{ background: '#ef4444', color: 'white', padding: '4px 12px', border: 'none', borderRadius: '4px' }}
                >
                  Hủy
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default App;