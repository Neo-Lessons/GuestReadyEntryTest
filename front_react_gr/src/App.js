import { useEffect, useState } from 'react'
import './App.css';

function App() {
  const [reservation, setReservations] = useState([])
  
  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/v1/')
      //  .then(res => console.log(res))
      .then(res => res.json())
      // .then(data => console.log(data))
      .then(data => setReservations(data))
  }, [])

  return (
    <div className="App">
      <h1>Reservations</h1>
      <div className="table-wrapper">
        <table className="fl-table">
          <thead>
            <tr>
              <th>Rental object</th>
              <th>Reservation ID</th>
              <th>Checkin</th>
              <th>Checkout</th>
              <th>Previous Reservation, ID</th>
            </tr>
          </thead>
          <tbody>
            {reservation && reservation.map(reserv => (
              <tr key={reserv.id}>
                <td>{reserv.id}</td>
                <td>{reserv.rental.name}</td>
                <td>{reserv.checkin}</td>
                <td>{reserv.checkout}</td>
                <td>{reserv.id_prev}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;
