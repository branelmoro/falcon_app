import hashlib
from ..resources.redis import redis as redisCrud

redisCrud("sessionDb")

class Session(object):

	__session_id = None

	def __init__(self, req):
		self.__session_db = redisCrud("sessionDb")


	def generateUniqueIdFromKey($key = null):
		if($key === null) {
			$key = "random number + timestamp";
		}
		while($this->RedisCache->exists($key)) {
			$key = $this->generateUniqueIdFromKey($key);
		}
		return md5($key);


	def load(self, req):
		# load session
		if(isset($_COOKIE["x-session"])) {
			if($this->RedisCache->exists($_COOKIE["x-session"])) {
				$this->sessionData = json_decode($this->RedisCache->get($_COOKIE["x-session"]), true);
				$this->session_id = $_COOKIE["x-session"];
			} else {
				// unset session cookie
				setcookie("x-session", $this->session_id, time()-100000);
			}
		}
		pass

	def exists(self):
		return (self->session_id is not None);



<?php
namespace App\Library;

use App\Resources\RedisCache;

use Psr\Container\ContainerInterface;
// ini_set('display_errors', 1);
// ini_set('display_startup_errors', 1);
// error_reporting(E_ALL);
class Session {

	private $sessionData = [];

	private $session_id = null;

	private $RedisCache = null;

	private $container = null;

	public function __construct(ContainerInterface $container) {
		$this->container = $container;
		$this->RedisCache = new RedisCache($this->container->get('settings')["redis"]["sessionDb"]);

		// load existing session
		$this->load();
	}

	private function generateUniqueIdFromKey($key = null) {
		if($key === null) {
			$key = "random number + timestamp";
		}
		while($this->RedisCache->exists($key)) {
			$key = $this->generateUniqueIdFromKey($key);
		}
		return md5($key);
	}

	public function exists() {
		return ($this->session_id !== null);
	}

	public function init($session_id = null, $expiry = 900) {
		$this->session_id = $this->generateUniqueIdFromKey($session_id);

		// create cookie and save session in cache
		$this->write_session_to_cache($expiry);
		setcookie("x-session", $this->session_id, time()+$expiry);
	}

	private function load() {
		// load session from cookie
		if(isset($_COOKIE["x-session"])) {
			if($this->RedisCache->exists($_COOKIE["x-session"])) {
				$this->sessionData = json_decode($this->RedisCache->get($_COOKIE["x-session"]), true);
				$this->session_id = $_COOKIE["x-session"];
			} else {
				// unset session cookie
				setcookie("x-session", $this->session_id, time()-100000);
			}
		}
	}

	public function setData(Array $arr) {
		$this->sessionData = array_merge($this->sessionData, $arr);
		$ttl = $this->RedisCache->ttl($this->session_id);
		return $this->write_session_to_cache($ttl);
	}

	public function getData() {
		return $this->sessionData;
	}

	public function set($key, $value) {
		$this->sessionData[$key] = $value;
		$ttl = $this->RedisCache->ttl($this->session_id);
		$this->write_session_to_cache();
	}

	private function write_session_to_cache($expiry) {
		$this->RedisCache->set($this->session_id, json_encode($this->sessionData), $expiry);
	}

	public function get($key) {
		return $this->sessionData[$key];
	}

	public function refresh(Array $data) {
		$this->sessionData = array_merge($this->sessionData, $arr);
		$this->init($data["refreshToken"], $data["refreshTokenExpiry"]);
		$this->setData($data);
	}

	public function destroy() {
		$this->RedisCache->delete($this->session_id);
		$this->session_id = null;
		$this->sessionData = [];
		setcookie("x-session", $this->session_id, time()-100000);
		unset($_COOKIE["x-session"]);
	}

}