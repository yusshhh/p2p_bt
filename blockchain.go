package main

import (
	"crypto/sha256"
	"encoding/json"
	"fmt"
	"net/http"
	"sync"
	"time"
)

type Block struct {
	Index        int    `json:"index"`
	Timestamp    string `json:"timestamp"`
	FileName     string `json:"file_name"`
	FileHash     string `json:"file_hash"`
	PreviousHash string `json:"previous_hash"`
	Hash         string `json:"hash"`
}

type Blockchain struct {
	Blocks []Block
	mu     sync.Mutex
}

var blockchain = Blockchain{
	Blocks: []Block{createGenesisBlock()},
}

func createGenesisBlock() Block {
	return Block{
		Index:        0,
		Timestamp:    time.Now().String(),
		FileName:     "Genesis Block",
		FileHash:     "",
		PreviousHash: "0",
		Hash:         calculateHash(0, time.Now().String(), "Genesis Block", "", "0"),
	}
}

func calculateHash(index int, timestamp, fileName, fileHash, previousHash string) string {
	record := fmt.Sprintf("%d%s%s%s%s", index, timestamp, fileName, fileHash, previousHash)
	h := sha256.New()
	h.Write([]byte(record))
	return fmt.Sprintf("%x", h.Sum(nil))
}

func (bc *Blockchain) AddBlock(fileName, fileHash string) {
	bc.mu.Lock()
	defer bc.mu.Unlock()

	lastBlock := bc.Blocks[len(bc.Blocks)-1]
	newBlock := Block{
		Index:        len(bc.Blocks),
		Timestamp:    time.Now().String(),
		FileName:     fileName,
		FileHash:     fileHash,
		PreviousHash: lastBlock.Hash,
		Hash:         calculateHash(len(bc.Blocks), time.Now().String(), fileName, fileHash, lastBlock.Hash),
	}
	bc.Blocks = append(bc.Blocks, newBlock)
}

func (bc *Blockchain) GetBlockchain() []Block {
	bc.mu.Lock()
	defer bc.mu.Unlock()
	return bc.Blocks
}

func (bc *Blockchain) Validate() bool {
	bc.mu.Lock()
	defer bc.mu.Unlock()

	for i := 1; i < len(bc.Blocks); i++ {
		currentBlock := bc.Blocks[i]
		previousBlock := bc.Blocks[i-1]

		if currentBlock.Hash != calculateHash(currentBlock.Index, currentBlock.Timestamp, currentBlock.FileName, currentBlock.FileHash, currentBlock.PreviousHash) {
			return false
		}

		if currentBlock.PreviousHash != previousBlock.Hash {
			return false
		}
	}
	return true
}

func handleAddBlock(w http.ResponseWriter, r *http.Request) {
	var data struct {
		FileName string `json:"file_name"`
		FileHash string `json:"file_hash"`
	}
	if err := json.NewDecoder(r.Body).Decode(&data); err != nil {
		http.Error(w, "Invalid request body", http.StatusBadRequest)
		return
	}
	blockchain.AddBlock(data.FileName, data.FileHash)
	w.WriteHeader(http.StatusCreated)
}

func handleGetBlockchain(w http.ResponseWriter, r *http.Request) {
	json.NewEncoder(w).Encode(blockchain.GetBlockchain())
}

func handleValidate(w http.ResponseWriter, r *http.Request) {
	if blockchain.Validate() {
		w.Write([]byte("Blockchain is valid"))
	} else {
		w.Write([]byte("Blockchain is invalid"))
	}
}

func main() {
	http.HandleFunc("/add_block", handleAddBlock)
	http.HandleFunc("/blockchain", handleGetBlockchain)
	http.HandleFunc("/validate", handleValidate)

	fmt.Println("Blockchain server running on port 8080...")
	http.ListenAndServe(":8080", nil)
}
