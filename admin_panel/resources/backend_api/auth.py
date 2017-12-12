import pycurl
from .resource_api import BACKEND_API

class Auth(BACKEND_API):


	pass


<?php
namespace App\Resources;

use Psr\Container\ContainerInterface;

class AppApi {

	private $container;

	private $client_credentials;

	private $authUrl = null;

	private $headers = [
		'Content-Type: application/json'
	];

	// constructor receives container instance
	public function __construct(ContainerInterface $container) {
		$this->container = $container;
		// fetch api url from app container
		$this->authUrl = $container->get('settings')['appAuth'];
		$this->client_credentials = $this->container->get('settings')['clientApp'];
	}

	public function get($path) {
		return $this->getDataFromApi("GET", $path);
	}

	public function post($path, $data = null) {
		return $this->getDataFromApi("POST", $path, $data);
	}

	public function put($path, $data = null) {
		return $this->getDataFromApi("PUT", $path, $data);
	}

	public function delete($path, $data) {
		return $this->getDataFromApi("DELETE", $path, $data);
	}

	private function getToken() {
		if($this->container->session->exists()) {
			$accessToken = $this->container->session->get("accessToken");
			if($accessToken) {
				return $accessToken;
			}
		}
		// if token not found get token from client app session
		$client_session_id = md5(json_encode($this->client_credentials));
		$client_data = $this->container->appCache->get($client_session_id);
		if($client_data == null) {
			$client_data = $this->grant_type_client_credentials();
		} else {
			$client_data = json_decode($client_data, true);
		}
		return $client_data["accessToken"];
	}

	public function auth($data) {
		return $this->grant_type_password($data);
	}

	private function grant_type_authorization_code($data) {
		// not needed for our own apps
	}

	private function grant_type_password($data) {
		$url = $this->container->get('settings')['appAuth']."/token/";

		$this->headers = [
			'Content-Type: application/json',
			'Authorization: Basic '.base64_encode(implode(":", $this->client_credentials))
		];
		$data["grant_type"] = "password";
		$arrResponce = $this->execute("POST", $url, $data);
		// save token and refresh token

		if($arrResponce["httpcode"] == 400) {
			return false;
		} else {
			// no error ocurred
			$this->startSession($arrResponce["response"]);
			return $arrResponce["response"]["accessToken"];
		}
	}

	private function grant_type_client_credentials() {
		$url = $this->container->get('settings')['appAuth']."/token/";

		$this->headers = [
			'Content-Type: application/json',
			'Authorization: Basic '.base64_encode(implode(":", $this->client_credentials))
		];
		$data = array();
		$data["grant_type"] = "client_credentials";
		$arrResponce = $this->execute("POST", $url, $data);
		// save token and refresh token

		if($arrResponce["httpcode"] == 400) {
			throw new \Exception("Clientapp authorization failed");
		} else {
			// save in session
			$client_session_id = md5(json_encode($this->client_credentials));
			$this->container->appCache->set($client_session_id, json_encode($arrResponce["response"]), $arrResponce["response"]["accessTokenExpiry"] - 5);
			return $arrResponce["response"];
		}
	}

	private function grant_type_refresh_token() {
		$url = $this->container->get('settings')['appAuth']."/token/";

		$this->headers = [
			'Content-Type: application/json',
			'Authorization: Basic '.base64_encode(implode(":", $this->client_credentials))
		];

		$data = array();
		$data["refresh_token"] = $this->container->session->get("refreshToken");
		$data["grant_type"] = "refresh_token";

		$arrResponce = $this->execute("POST", $url, $data);

		if($arrResponce["httpcode"] == 400) {
			return false;
		} else {
			// no error ocurred
			$this->container->session->refresh($arrResponce["response"]);
			return $arrResponce["response"];
		}
	}

	private function startSession($data) {
		$this->container->session->init($data["refreshToken"], $data["refreshTokenExpiry"]);
		$this->container->session->setData($data);
	}

	private function getDataFromApi($method, $path, $data = null) {
		$url = $this->container->get('settings')['appApi'].$path;
		$this->headers = [
			'Content-Type: application/json',
			'access-token: "'.$this->getToken().'"'
		];
		$arrResponce = $this->execute($method, $url, $data);

		if($arrResponce["httpcode"] === 401) {
			// unauthorised token found

			if($this->container->session->exists()) {
				// this is user session

				$refreshToken = $this->container->session->get("refreshToken");
				if($refreshToken) {
					// this is registered user
					$tokenData = $this->grant_type_refresh_token();
					if($tokenData === false) {
						// refresh token expired, destroy user session vars and get client app token
						$this->container->session->destroySessionVars();
						$token = $this->getToken();
					} else {
						$token = $tokenData["accessToken"];
					}
				} else {
					// this is guest user, get client app accessToken fro this user
					$token = $this->getToken();
				}
			} else {
				// this is client app session
				$token = $this->getToken();
			}

			$this->headers = array(
				'Content-Type: application/json',
				'access-token: "'.$token.'"'
			);
			$arrResponce = $this->execute($method, $url, $data);
		}

		return $arrResponce;

	}

	public function destroyTokens($data) {
		$this->headers = [
			'Content-Type: application/json'
		];
		$url = $this->container->get('settings')['appAuth']."/token/";
		return $this->execute("DELETE", $url, $data);
	}

	private function execute($method, $url, $data = null) {

		$ch = curl_init();
		curl_setopt($ch, CURLOPT_URL, $url);
		if(is_array($data)) {
			$data_json = json_encode($data);
			$this->headers[] = 'Content-Length: ' . strlen($data_json);
			curl_setopt($ch, CURLOPT_POSTFIELDS, $data_json);
		}
		curl_setopt($ch, CURLOPT_HTTPHEADER, $this->headers);
		// curl_setopt($ch, CURLOPT_HEADER, true);
		curl_setopt($ch, CURLOPT_CUSTOMREQUEST, $method);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		$response  = json_decode(curl_exec($ch), true);
		$error_no = curl_errno($ch);
		$httpcode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
		curl_close($ch);

		print_r([
			"response" => $response,
			"error_no" => $error_no,
			"httpcode" => $httpcode
		]);

		if($response === null ) {
			throw new \Exception("Backend Api Connection Issue");
		}

		if(in_array($httpcode, [500,501,502,503,504,505])) {
			throw new \Exception("Backend Api Server Error");
		}

		return [
			"response" => $response,
			"error_no" => $error_no,
			"httpcode" => $httpcode
		];
	}

}