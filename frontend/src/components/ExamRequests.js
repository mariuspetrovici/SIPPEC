import React, { useState, useEffect } from 'react';
import { Box, Typography, TextField, MenuItem, Table, TableBody, TableCell, TableHead, TableRow } from '@mui/material';
import axios from 'axios';
import useAuthStore from '../store/authStore';
import moment from 'moment';

function ExamRequests() {
  const { token, user } = useAuthStore();
  const [exams, setExams] = useState([]);
  const [courses, setCourses] = useState([]);
  const [selectedCourse, setSelectedCourse] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [examsRes, coursesRes] = await Promise.all([
          axios.get('http://localhost:8000/exams_schedule/', { headers: { Authorization: `Bearer ${token}` } }),
          axios.get('http://localhost:8000/courses/', { headers: { Authorization: `Bearer ${token}` } }),
        ]);
        setExams(examsRes.data);
        setCourses(coursesRes.data);
        // Set default filter for teachers
        if (user?.type === 'TEACHER') {
          const teacherCourse = coursesRes.data.find(course => course.owner_user_id === user.id);
          setSelectedCourse(teacherCourse?.id || '');
        }
      } catch (error) {
        console.error('Failed to fetch data:', error);
      }
    };
    fetchData();
  }, [token, user]);

  const filteredExams = selectedCourse
    ? exams.filter(exam => exam.course_id === parseInt(selectedCourse))
    : exams;

  const isStudent = user?.type === 'STUDENT';
  const userExams = isStudent ? filteredExams.filter(exam => exam.user_id === user.id) : filteredExams;

  return (
    <Box sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Exam Requests</Typography>
      {!isStudent && (
        <TextField
          select
          label="Filter by Course"
          value={selectedCourse}
          onChange={(e) => setSelectedCourse(e.target.value)}
          sx={{ mb: 2, minWidth: 200 }}
        >
          <MenuItem value="">All Courses</MenuItem>
          {courses.map(course => (
            <MenuItem key={course.id} value={course.id}>{course.name}</MenuItem>
          ))}
        </TextField>
      )}
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Course ID</TableCell>
            <TableCell>Group ID</TableCell>
            <TableCell>Date</TableCell>
            <TableCell>Status</TableCell>
            <TableCell>User ID</TableCell>
            <TableCell>Classroom ID</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {userExams.map(exam => (
            <TableRow key={exam.id}>
              <TableCell>{exam.course_id}</TableCell>
              <TableCell>{exam.group_id}</TableCell>
              <TableCell>{moment(exam.date).format('YYYY-MM-DD HH:mm')}</TableCell>
              <TableCell>{exam.status}</TableCell>
              <TableCell>{exam.user_id}</TableCell>
              <TableCell>{exam.classroom_id}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Box>
  );
}

export default ExamRequests;