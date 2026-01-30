from datetime import datetime, timezone, timedelta


def _create_patient(client, email: str):
    r = client.post(
        "/patients",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": email,
            "phone": "99999",
        },
    )
    assert r.status_code == 201, r.text
    return r.json()["id"]


def _create_doctor(client):
    r = client.post(
        "/doctors",
        json={
            "full_name": "Dr Test",
            "specialization": "General",
        },
    )
    assert r.status_code == 201, r.text
    return r.json()["id"]


def test_rejects_naive_datetime(client):
    patient_id = _create_patient(client, "a@example.com")
    doctor_id = _create_doctor(client)

    # No timezone offset -> schema validation should reject (FastAPI returns 422)
    r = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "start_time": "2026-02-01T10:00:00",
            "duration_minutes": 30,
        },
    )
    assert r.status_code == 422, r.text


def test_rejects_past_appointment(client):
    patient_id = _create_patient(client, "b@example.com")
    doctor_id = _create_doctor(client)

    past = datetime.now(timezone.utc) - timedelta(minutes=10)

    r = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "start_time": past.isoformat(),
            "duration_minutes": 30,
        },
    )
    assert r.status_code == 400, r.text


def test_prevents_overlapping_appointments(client):
    patient_id = _create_patient(client, "c@example.com")
    doctor_id = _create_doctor(client)

    start1 = datetime.now(timezone.utc) + timedelta(minutes=120)  # future
    start2 = start1 + timedelta(minutes=15)  # overlaps with 30 min appt

    r1 = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "start_time": start1.isoformat(),
            "duration_minutes": 30,
        },
    )
    assert r1.status_code == 201, r1.text

    r2 = client.post(
        "/appointments",
        json={
            "patient_id": patient_id,
            "doctor_id": doctor_id,
            "start_time": start2.isoformat(),
            "duration_minutes": 30,
        },
    )
    assert r2.status_code == 409, r2.text
