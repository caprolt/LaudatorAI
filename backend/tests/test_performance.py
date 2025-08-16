"""Performance tests for API endpoints."""

import time
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import get_db, Base

# Create in-memory database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class PerformanceTest:
    """Performance testing utilities."""
    
    @staticmethod
    def measure_response_time(func, *args, **kwargs):
        """Measure the response time of a function."""
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        return result, (end_time - start_time) * 1000  # Convert to milliseconds
    
    @staticmethod
    def run_concurrent_requests(func, num_requests=10, *args, **kwargs):
        """Run multiple concurrent requests and measure performance."""
        response_times = []
        results = []
        
        with ThreadPoolExecutor(max_workers=min(num_requests, 10)) as executor:
            futures = [executor.submit(func, *args, **kwargs) for _ in range(num_requests)]
            
            for future in as_completed(futures):
                try:
                    result, response_time = future.result()
                    results.append(result)
                    response_times.append(response_time)
                except Exception as e:
                    print(f"Request failed: {e}")
        
        return results, response_times


class TestAPIPerformance:
    """Test API performance under various conditions."""
    
    def test_health_endpoint_performance(self):
        """Test health endpoint performance."""
        print("🔍 Testing health endpoint performance...")
        
        def health_request():
            return self.measure_response_time(client.get, "/health")
        
        results, response_times = self.run_concurrent_requests(health_request, 20)
        
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        p95_time = statistics.quantiles(response_times, n=20)[18]  # 95th percentile
        
        print(f"✅ Health endpoint performance:")
        print(f"   Average: {avg_time:.2f}ms")
        print(f"   Min: {min_time:.2f}ms")
        print(f"   Max: {max_time:.2f}ms")
        print(f"   95th percentile: {p95_time:.2f}ms")
        
        # Assert reasonable performance
        assert avg_time < 100, f"Average response time too high: {avg_time}ms"
        assert p95_time < 200, f"95th percentile response time too high: {p95_time}ms"
    
    def test_job_extraction_performance(self):
        """Test job extraction endpoint performance."""
        print("🔍 Testing job extraction performance...")
        
        def job_extraction_request():
            return self.measure_response_time(
                client.post, 
                "/api/v1/jobs/extract", 
                json={"url": "https://example.com/job"}
            )
        
        results, response_times = self.run_concurrent_requests(job_extraction_request, 10)
        
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        p95_time = statistics.quantiles(response_times, n=10)[8]  # 95th percentile
        
        print(f"✅ Job extraction performance:")
        print(f"   Average: {avg_time:.2f}ms")
        print(f"   Min: {min_time:.2f}ms")
        print(f"   Max: {max_time:.2f}ms")
        print(f"   95th percentile: {p95_time:.2f}ms")
        
        # Assert reasonable performance
        assert avg_time < 500, f"Average response time too high: {avg_time}ms"
        assert p95_time < 1000, f"95th percentile response time too high: {p95_time}ms"
    
    def test_resume_upload_performance(self):
        """Test resume upload endpoint performance."""
        print("🔍 Testing resume upload performance...")
        
        def resume_upload_request():
            files = {"file": ("test.pdf", b"fake pdf content", "application/pdf")}
            return self.measure_response_time(
                client.post, 
                "/api/v1/resumes/upload", 
                files=files
            )
        
        results, response_times = self.run_concurrent_requests(resume_upload_request, 5)
        
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        p95_time = statistics.quantiles(response_times, n=5)[4]  # 95th percentile
        
        print(f"✅ Resume upload performance:")
        print(f"   Average: {avg_time:.2f}ms")
        print(f"   Min: {min_time:.2f}ms")
        print(f"   Max: {max_time:.2f}ms")
        print(f"   95th percentile: {p95_time:.2f}ms")
        
        # Assert reasonable performance
        assert avg_time < 1000, f"Average response time too high: {avg_time}ms"
        assert p95_time < 2000, f"95th percentile response time too high: {p95_time}ms"
    
    def test_application_creation_performance(self):
        """Test application creation performance."""
        print("🔍 Testing application creation performance...")
        
        # Pre-create job and resume for testing
        job_response = client.post("/api/v1/jobs/extract", json={"url": "https://example.com/test"})
        job_id = job_response.json()["id"]
        
        files = {"file": ("test.pdf", b"content", "application/pdf")}
        resume_response = client.post("/api/v1/resumes/upload", files=files)
        resume_id = resume_response.json()["id"]
        
        def application_creation_request():
            return self.measure_response_time(
                client.post, 
                "/api/v1/applications", 
                json={"job_id": job_id, "resume_id": resume_id}
            )
        
        results, response_times = self.run_concurrent_requests(application_creation_request, 5)
        
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        p95_time = statistics.quantiles(response_times, n=5)[4]  # 95th percentile
        
        print(f"✅ Application creation performance:")
        print(f"   Average: {avg_time:.2f}ms")
        print(f"   Min: {min_time:.2f}ms")
        print(f"   Max: {max_time:.2f}ms")
        print(f"   95th percentile: {p95_time:.2f}ms")
        
        # Assert reasonable performance
        assert avg_time < 500, f"Average response time too high: {avg_time}ms"
        assert p95_time < 1000, f"95th percentile response time too high: {p95_time}ms"
    
    def test_database_query_performance(self):
        """Test database query performance."""
        print("🔍 Testing database query performance...")
        
        # Create some test data
        for i in range(10):
            client.post("/api/v1/jobs/extract", json={"url": f"https://example.com/job{i}"})
        
        def list_jobs_request():
            return self.measure_response_time(client.get, "/api/v1/jobs")
        
        results, response_times = self.run_concurrent_requests(list_jobs_request, 10)
        
        avg_time = statistics.mean(response_times)
        min_time = min(response_times)
        max_time = max(response_times)
        p95_time = statistics.quantiles(response_times, n=10)[8]  # 95th percentile
        
        print(f"✅ Database query performance:")
        print(f"   Average: {avg_time:.2f}ms")
        print(f"   Min: {min_time:.2f}ms")
        print(f"   Max: {max_time:.2f}ms")
        print(f"   95th percentile: {p95_time:.2f}ms")
        
        # Assert reasonable performance
        assert avg_time < 200, f"Average response time too high: {avg_time}ms"
        assert p95_time < 500, f"95th percentile response time too high: {p95_time}ms"


class TestLoadHandling:
    """Test how the API handles load."""
    
    def test_concurrent_job_extractions(self):
        """Test concurrent job extractions."""
        print("🔍 Testing concurrent job extractions...")
        
        def job_extraction_request(job_id):
            return self.measure_response_time(
                client.post, 
                "/api/v1/jobs/extract", 
                json={"url": f"https://example.com/concurrent-job-{job_id}"}
            )
        
        # Test with 20 concurrent requests
        results, response_times = self.run_concurrent_requests(
            lambda: job_extraction_request(time.time()), 20
        )
        
        successful_requests = len([r for r in results if r[0].status_code == 200])
        avg_time = statistics.mean(response_times)
        
        print(f"✅ Concurrent job extractions:")
        print(f"   Successful requests: {successful_requests}/20")
        print(f"   Average response time: {avg_time:.2f}ms")
        
        # Assert most requests succeed
        assert successful_requests >= 18, f"Too many failed requests: {20 - successful_requests}"
    
    def test_mixed_workload(self):
        """Test mixed workload performance."""
        print("🔍 Testing mixed workload performance...")
        
        def health_request():
            return self.measure_response_time(client.get, "/health")
        
        def job_request():
            return self.measure_response_time(
                client.post, 
                "/api/v1/jobs/extract", 
                json={"url": f"https://example.com/mixed-{time.time()}"}
            )
        
        # Run mixed workload
        health_results, health_times = self.run_concurrent_requests(health_request, 10)
        job_results, job_times = self.run_concurrent_requests(job_request, 5)
        
        avg_health_time = statistics.mean(health_times)
        avg_job_time = statistics.mean(job_times)
        
        print(f"✅ Mixed workload performance:")
        print(f"   Health endpoint average: {avg_health_time:.2f}ms")
        print(f"   Job extraction average: {avg_job_time:.2f}ms")
        
        # Assert reasonable performance under mixed load
        assert avg_health_time < 150, f"Health endpoint too slow under load: {avg_health_time}ms"
        assert avg_job_time < 600, f"Job extraction too slow under load: {avg_job_time}ms"


if __name__ == "__main__":
    print("🚀 Starting performance tests...")
    
    # Run performance tests
    perf_test = TestAPIPerformance()
    perf_test.test_health_endpoint_performance()
    perf_test.test_job_extraction_performance()
    perf_test.test_resume_upload_performance()
    perf_test.test_application_creation_performance()
    perf_test.test_database_query_performance()
    
    # Run load tests
    load_test = TestLoadHandling()
    load_test.test_concurrent_job_extractions()
    load_test.test_mixed_workload()
    
    print("🎉 All performance tests completed successfully!")
